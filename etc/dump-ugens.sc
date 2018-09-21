(
    UGen.allSubclasses.asSortedList({
        arg a, b; a.name < b.name;
    }).do({
        arg ugen;
        ugen.postln;
        ugen.superclass.postln;
        ugen.class.methods.do({
            arg method;
            method.postln;
            method.keyValuePairsFromArgs.asDict.postln;
        });
    })
)
