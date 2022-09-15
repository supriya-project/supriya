import supriya


def test_01():

    with supriya.SynthDefBuilder(out=0, value=0.5) as builder:
        supriya.ugens.Out.ar(
            bus=builder["out"], source=supriya.ugens.DC.ar(source=builder["value"])
        )
    synthdef_A = builder.build(name="synthdef_A")

    with supriya.SynthDefBuilder(out=0, value=-0.3) as builder:
        supriya.ugens.Out.ar(
            bus=builder["out"], source=supriya.ugens.DC.ar(source=builder["value"])
        )
    synthdef_B = builder.build(name="synthdef_B")

    request = supriya.commands.SynthDefReceiveRequest(
        synthdefs=[synthdef_A],
        callback=supriya.commands.RequestBundle(
            contents=[
                supriya.commands.GroupNewRequest(
                    items=[
                        supriya.commands.GroupNewRequest.Item(
                            node_id=1000, target_node_id=1
                        )
                    ]
                ),
                supriya.commands.SynthNewRequest(
                    node_id=1001, synthdef=synthdef_A, target_node_id=1000
                ),
                supriya.commands.SynthDefReceiveRequest(
                    synthdefs=[synthdef_B],
                    callback=supriya.commands.RequestBundle(
                        contents=[
                            supriya.commands.SynthNewRequest(
                                add_action=supriya.AddAction.ADD_BEFORE,
                                node_id=1002,
                                synthdef=synthdef_B,
                                target_node_id=1001,
                            ),
                            supriya.commands.NodeRunRequest(
                                node_id_run_flag_pairs=[(1002, False)]
                            ),
                        ]
                    ),
                ),
            ]
        ),
    )

    assert list(request._linearize()) == [
        supriya.commands.SynthDefReceiveRequest(synthdefs=(synthdef_A,)),
        supriya.commands.GroupNewRequest(
            items=[
                supriya.commands.GroupNewRequest.Item(
                    add_action=supriya.AddAction.ADD_TO_HEAD,
                    node_id=1000,
                    target_node_id=1,
                )
            ]
        ),
        supriya.commands.SynthNewRequest(
            add_action=supriya.AddAction.ADD_TO_HEAD,
            node_id=1001,
            synthdef=synthdef_A,
            target_node_id=1000,
        ),
        supriya.commands.SynthDefReceiveRequest(synthdefs=(synthdef_B,)),
        supriya.commands.SynthNewRequest(
            add_action=supriya.AddAction.ADD_BEFORE,
            node_id=1002,
            synthdef=synthdef_B,
            target_node_id=1001,
        ),
        supriya.commands.NodeRunRequest(node_id_run_flag_pairs=((1002, False),)),
    ]
