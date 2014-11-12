# -*- encoding: utf-8 -*-
import importlib
import inspect
from docutils import nodes
from sphinx import addnodes


def doctree_read(app, doctree):

    classes_to_attributes = {}

    def get_unique_parts(parts):
        unique_parts = [parts[0]]
        for part in parts[1:]:
            if part != unique_parts[-1]:
                unique_parts.append(part)
            else:
                break
        return unique_parts

    for desc_node in doctree.traverse(addnodes.desc):
        if desc_node.get('domain') != 'py':
            continue

        signature_node = desc_node.traverse(addnodes.desc_signature)[0]
        module_name = signature_node.get('module')
        object_name = signature_node.get('fullname')
        object_type = desc_node.get('objtype')
        module = importlib.import_module(module_name)

        if object_type == 'class':
            cls = getattr(module, object_name, None)
            if cls is None:
                continue
            if cls not in classes_to_attributes:
                classes_to_attributes[cls] = {}
                attributes = inspect.classify_class_attrs(cls)
                for attribute in attributes:
                    classes_to_attributes[cls][attribute.name] = attribute
            if inspect.isabstract(cls):
                labelnode = addnodes.only(expr='html')
                labelnode.append(nodes.emphasis(
                    'abstract ',
                    'abstract ',
                    classes=['property'],
                    ))
                signature_node.insert(0, labelnode)

        elif object_type in ('method', 'attribute', 'staticmethod', 'classmethod'):
            cls_name, attr_name = object_name.split('.')
            cls = getattr(module, cls_name, None)
            if cls is None:
                continue
            attr = getattr(cls, attr_name)
            inspected_attr = classes_to_attributes[cls][attr_name]
            label_node = addnodes.only(expr='html')
            defining_class = inspected_attr.defining_class
            if defining_class != cls:
                addname_node = signature_node.traverse(
                    addnodes.desc_addname)[0]
                if defining_class.__module__.startswith('supriya'):
                    reftarget = defining_class.__module__
                else:
                    reftarget = '{}.{}'.format(
                        defining_class.__module__,
                        defining_class.__name__,
                        )
                xref_node = addnodes.pending_xref(
                    '',
                    refdomain='py',
                    refexplicit=True,
                    reftype='class',
                    reftarget=reftarget,
                    )
                xref_node.append(nodes.literal(
                    '',
                    '{}'.format(defining_class.__name__),
                    classes=['descclassname'],
                    ))
                html_only_class_name_node = addnodes.only(expr='html')
                html_only_class_name_node.append(nodes.Text('('))
                html_only_class_name_node.append(xref_node)
                html_only_class_name_node.append(nodes.Text(').'))
                latex_only_class_name_node = addnodes.only(expr='latex')
                latex_only_class_name_node.append(nodes.Text(
                    '({}).'.format(defining_class.__name__),
                    ))
                addname_node.clear()
                addname_node.append(html_only_class_name_node)
                addname_node.append(latex_only_class_name_node)
                #label_node.append(nodes.emphasis(
                #    'inherited ',
                #    'inherited ',
                #    classes=['property'],
                #    ))
            if getattr(attr, '__isabstractmethod__', False):
                label_node.append(nodes.emphasis(
                    'abstract ',
                    'abstract ',
                    classes=['property'],
                    ))
            if hasattr(attr, 'im_self') and attr.im_self is not None:
                signature_node.pop(0)
                label_node.append(nodes.emphasis(
                    'classmethod ',
                    'classmethod ',
                    classes=['property'],
                    ))
            signature_node.insert(0, label_node)


def setup(app):
    app.connect('doctree-read', doctree_read)
    app.add_javascript('copybutton.js')
    app.add_stylesheet('supriya.css')