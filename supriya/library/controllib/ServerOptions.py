class ServerOptions(object):
    r'''SuperCollider server option configuration.

    ::

        >>> from supriya import controllib
        >>> options = controllib.ServerOptions()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_blockSize',
        '_hardwareBufferSize',
        '_inDevice',
        '_initialNodeID',
        '_inputStreamsEnabled',
        '_loadDefs',
        '_maxNodes',
        '_maxSynthDefs',
        '_memSize',
        '_memoryLocking',
        '_numAudioBusChannels',
        '_numBuffers',
        '_numControlBusChannels',
        '_numInputBusChannels',
        '_numOutputBusChannels',
        '_numPrivateAudioBusChannels',
        '_numRGens',
        '_numWireBufs',
        '_outDevice',
        '_outputStreamsEnabled',
        '_protocol',
        '_remoteControlVolume',
        '_restrictedPath',
        '_sampleRate',
        '_verbosity',
        '_zeroConf',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        blockSize=64,
        hardwareBufferSize=None,
        inDevice=None,
        initialNodeID=1000,
        inputStreamsEnabled=False,
        loadDefs=True,
        maxNodes=1024,
        maxSynthDefs=1024,
        memSize=8192,
        memoryLocking=False,
        numAudioBusChannels=128,
        numBuffers=1024,
        numControlBusChannels=4096,
        numInputBusChannels=8,
        numOutputBusChannels=8,
        numRGens=64,
        numWireBufs=64,
        outDevice=None,
        outputStreamsEnabled=False,
        protocol='udp',
        remoteControlVolume=False,
        restrictedPath=None,
        sampleRate=None,
        verbosity=0,
        zeroConf=False,
        ):
        # setup up basic channels
        self._numAudioBusChannels = 128
        self._numBuffers = 1026
        self._numControlBusChannels = 4096
        self._numInputBusChannels = 8
        self._numOutputBusChannels = 8
        self._numPrivateAudioBusChannels = 112

        self.numAudioBusChannels = int(numAudioBusChannels)
        self.numBuffers = int(numBuffers)
        self.numInputBusChannels = int(numInputBusChannels)
        self.numOutputBusChannels = int(numOutputBusChannels)

        self._blockSize = int(blockSize)
        self._hardwareBufferSize = hardwareBufferSize
        self._inDevice = inDevice
        self._initialNodeID = int(initialNodeID)
        self._inputStreamsEnabled = bool(inputStreamsEnabled)
        self._loadDefs = loadDefs
        self._maxNodes = int(maxNodes)
        self._maxSynthDefs = int(maxSynthDefs)
        self._memSize = int(memSize)
        self._memoryLocking = bool(memoryLocking)
        self._numControlBusChannels = int(numControlBusChannels)
        self._numRGens = int(numRGens)
        self._numWireBufs = int(numWireBufs)
        self._outDevice = outDevice
        self._outputStreamsEnabled = bool(outputStreamsEnabled)
        self._protocol = protocol
        self._remoteControlVolume = remoteControlVolume
        self._restrictedPath = restrictedPath
        self._sampleRate = sampleRate
        self._verbosity = int(verbosity)
        self._zeroConf = bool(zeroConf)

    ### PRIVATE METHODS ###

    def _recalculate_channels(self):
        self._numAudioBusChannels = (
            self._numPrivateAudioBusChannels +
            self._numInputBusChannels +
            self._numOutputBusChannels
            )

    ### PUBLIC METHODS ###

    def as_options_string(self, port=57110):
        result = []

        if self.protocol == 'tcp':
            result.append('-t')
        else:
            result.append('-u')
        result.append(str(port))

        result.append('-a')
        result.append(
            self.numPrivateAudioBusChannels +
            self.numInputBusChannels +
            self.numOutputBusChannels
            )

        if self.numControlBusChannels != 4096:
            result.append('-c {}'.format(self.numControlBusChannels))

        if self.numInputBusChannels != 8:
            result.append('-i {}'.format(self.numInputBusChannels))

        if self.numOutputBusChannels != 8:
            result.append('-o {}'.format(self.numOutputBusChannels))

        if self.numBuffers != 1024:
            result.append('-b {}'.format(self.numBuffers))

        if self.maxNodes != 1024:
            result.append('-n {}'.format(self.maxNodes))

        if self.maxSynthDefs != 1024:
            result.append('-d {}'.format(self.maxSynthDefs))

        if self.blockSize != 64:
            result.append('-z {}'.format(self.blockSize))

        if self.hardwareBufferSize is not None:
            result.append('-Z {}'.format(int(self.hardwareBufferSize)))

        if self.memSize != 8192:
            result.append('-m {}'.format(self.memSize))

        if self.numRGens != 64:
            result.append('-r {}'.format(self.numRGens))

        if self.numWireBufs != 64:
            result.append('-w {}'.format(self.numWireBufs))

        if self.sampleRate is not None:
            result.append('-S {}'.format(int(self.sampleRate)))

        if not self.loadDefs:
            result.append('-D 0')

        if self.inputStreamsEnabled:
            result.append('-I {}'.format(self.inputStreamsEnabled))

        if self.outputStreamsEnabled:
            result.append('-O {}'.format(self.outputStreamsEnabled))

        r'''
        if ((thisProcess.platform.name!=\osx) or: {inDevice == outDevice})
        {
            if (inDevice.notNil,
            {
                result = result ++ " -H %".format(inDevice.quote);
            });
        }
        {
            result = result ++ " -H % %".format(inDevice.asString.quote, outDevice.asString.quote);
        };
        '''

        if 0 < self.verbosity:
            result.append('-v {}'.format(self.verbosity))

        if not self.zeroConf:
            result.append('-R 0')

        if self.restrictedPath is not None:
            result.append('-P {}'.format(self.restrictedPath))

        if self.memoryLocking:
            result.append('-L')

        r'''
        if (threads.notNil, {
            if (Server.program.asString.endsWith("supernova")) {
                result = result ++ " -T " ++ threads;
            }
        });
        '''

        options_string = ' '.join(str(x) for x in result)
        return options_string

    ### PUBLIC PROPERTIES ###

    @property
    def blockSize(self):
        return self._blockSize

    @property
    def firstPrivateBus(self):
        return self.numOutputBusChannels + self.numInputBusChannels

    @property
    def hardwareBufferSize(self):
        return self._hardwareBufferSize

    @property
    def inDevice(self):
        return self._inDevice

    @property
    def initialNodeID(self):
        return self._initialNodeID

    @property
    def inputStreamsEnabled(self):
        return self._inputStreamsEnabled

    @property
    def loadDefs(self):
        return self._loadDefs

    @property
    def maxNodes(self):
        return self._maxNodes

    @property
    def maxSynthDefs(self):
        return self._maxSynthDefs

    @property
    def memSize(self):
        return self._memSize

    @property
    def memoryLocking(self):
        return self._memoryLocking

    @property
    def numAudioBusChannels(self):
        return self._numAudioBusChannels

    @numAudioBusChannels.setter
    def numAudioBusChannels(self, expr):
        self._numAudioBusChannels = int(expr)
        self._numPrivateAudioBusChannels = (
            self._numAudioBusChannels -
            self._numInputBusChannels -
            self._numOutputBusChannels
            )

    @property
    def numBuffers(self):
        return self._numBuffers - 2

    @numBuffers.setter
    def numBuffers(self, expr):
        self._numBuffers = int(expr) + 2

    @property
    def numControlBusChannels(self):
        return self._numControlBusChannels

    @property
    def numInputBusChannels(self):
        return self._numInputBusChannels

    @numInputBusChannels.setter
    def numInputBusChannels(self, expr):
        self._numInputBusChannels = int(expr)
        self._recalculate_channels()

    @property
    def numOutputBusChannels(self):
        return self._numOutputBusChannels

    @numOutputBusChannels.setter
    def numOutputBusChannels(self, expr):
        self._numOutputBusChannels = int(expr)
        self._recalculate_channels()

    @property
    def numPrivateAudioBusChannels(self):
        return self._numPrivateAudioBusChannels

    @numPrivateAudioBusChannels.setter
    def numPrivateAudioBusChannels(self, expr):
        self._numPrivateAudioBusChannels = int(expr)
        self._recalculate_channels()

    @property
    def numRGens(self):
        return self._numRGens

    @property
    def numWireBufs(self):
        return self._numWireBufs

    @property
    def outDevice(self):
        return self._outDevice

    @property
    def outputStreamsEnabled(self):
        return self._outputStreamsEnabled

    @property
    def protocol(self):
        return self._protocol

    @property
    def remoteControlVolume(self):
        return self._remoteControlVolume

    @property
    def restrictedPath(self):
        return self._restrictedPath

    @property
    def sampleRate(self):
        return self._sampleRate

    @property
    def verbosity(self):
        return self._verbosity

    @property
    def zeroConf(self):
        return self._zeroConf
