from uqbar.strings import normalize

from supriya.xdaw import Application


def test_1():
    application = Application()
    context = application.add_context()
    track = context.add_track()
    assert str(application) == normalize(
        f"""
        <Application [OFFLINE] {hex(id(application))}>
            <Transport>
            <Controllers>
            <Contexts>
                <Context [...] {context.uuid}>
                    <Tracks [...]>
                        <Track [...] {track.uuid}>
                            <SubTracks [...]>
                            <SendTarget (0)>
                            <Receives [...]>
                            <Devices [...]>
                            <PreFaderSends [...]>
                            <PostFaderSends [...]>
                                <Send [...] {track.postfader_sends[0].uuid}>
                            <ReceiveTarget (0)>
                    <MasterTrack [...] {context.master_track.uuid}>
                        <SendTarget (1)>
                        <Receives [...]>
                        <Devices [...]>
                        <PreFaderSends [...]>
                        <PostFaderSends [...]>
                            <DirectOut [...] {context.master_track.postfader_sends[0].uuid}>
                        <ReceiveTarget (0)>
                    <CueTrack [...] {context.cue_track.uuid}>
                        <SendTarget (0)>
                        <Receives [...]>
                        <Devices [...]>
                        <PreFaderSends [...]>
                        <PostFaderSends [...]>
                            <DirectOut [...] {context.cue_track.postfader_sends[0].uuid}>
                        <ReceiveTarget (0)>
        """
    )


def test_2():
    application = Application()
    context = application.add_context()
    track = context.add_track()
    application.boot()
    assert str(application) == normalize(
        f"""
        <Application [REALTIME] {hex(id(application))}>
            <Transport>
            <Controllers>
            <Contexts>
                <Context [{context.node_proxy.identifier}] {context.uuid}>
                    <Tracks [{context.tracks.node_proxy.identifier}]>
                        <Track [{track.node_proxy.identifier}] {track.uuid}>
                            <SubTracks [{track.tracks.node_proxy.identifier}]>
                            <SendTarget (0)>
                            <Receives [{track.receives.node_proxy.identifier}]>
                            <Devices [{track.devices.node_proxy.identifier}]>
                            <PreFaderSends [{track.prefader_sends.node_proxy.identifier}]>
                            <PostFaderSends [{track.postfader_sends.node_proxy.identifier}]>
                                <Send [{track.postfader_sends[0].node_proxy.identifier}] {track.postfader_sends[0].uuid}>
                            <ReceiveTarget (0)>
                    <MasterTrack [{context.master_track.node_proxy.identifier}] {context.master_track.uuid}>
                        <SendTarget (1)>
                        <Receives [{context.master_track.receives.node_proxy.identifier}]>
                        <Devices [{context.master_track.devices.node_proxy.identifier}]>
                        <PreFaderSends [{context.master_track.prefader_sends.node_proxy.identifier}]>
                        <PostFaderSends [{context.master_track.postfader_sends.node_proxy.identifier}]>
                            <DirectOut [{context.master_track.postfader_sends[0].node_proxy.identifier}] {context.master_track.postfader_sends[0].uuid}>
                        <ReceiveTarget (0)>
                    <CueTrack [{context.cue_track.node_proxy.identifier}] {context.cue_track.uuid}>
                        <SendTarget (0)>
                        <Receives [{context.cue_track.receives.node_proxy.identifier}]>
                        <Devices [{context.cue_track.devices.node_proxy.identifier}]>
                        <PreFaderSends [{context.cue_track.prefader_sends.node_proxy.identifier}]>
                        <PostFaderSends [{context.cue_track.postfader_sends.node_proxy.identifier}]>
                            <DirectOut [{context.cue_track.postfader_sends[0].node_proxy.identifier}] {context.cue_track.postfader_sends[0].uuid}>
                        <ReceiveTarget (0)>
        """
    )
