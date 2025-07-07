import os
import platform

import pytest
from uqbar.strings import normalize

from supriya import SynthDef
from supriya.ugens import SuperColliderSynthDef, decompile_synthdef
from supriya.ugens.system import (
    amplitude_scope_audio_1,
    amplitude_scope_control_2,
    frequency_scope_lin_1,
    frequency_scope_lin_shm_1,
    frequency_scope_log_1,
    frequency_scope_log_shm_2,
    system_link_audio_1,
    system_link_audio_2,
)


@pytest.mark.parametrize(
    "synthdef, expected_str",
    [
        (
            system_link_audio_1,
            """
            synthdef:
                name: supriya:link-ar:1
                ugens:
                -   Control.kr:
                        done_action: 2.0
                        fade_time: 0.02
                        gate: 1.0
                        in_: 16.0
                        out: 0.0
                -   BinaryOpUGen(LESS_THAN_OR_EQUAL).kr:
                        left: Control.kr[1:fade_time]
                        right: 0.0
                -   EnvGen.kr:
                        gate: Control.kr[2:gate]
                        level_scale: 1.0
                        level_bias: 0.0
                        time_scale: Control.kr[1:fade_time]
                        done_action: Control.kr[0:done_action]
                        envelope[0]: BinaryOpUGen(LESS_THAN_OR_EQUAL).kr[0]
                        envelope[1]: 2.0
                        envelope[2]: 1.0
                        envelope[3]: -99.0
                        envelope[4]: 1.0
                        envelope[5]: 1.0
                        envelope[6]: 3.0
                        envelope[7]: 0.0
                        envelope[8]: 0.0
                        envelope[9]: 1.0
                        envelope[10]: 3.0
                        envelope[11]: 0.0
                -   InFeedback.ar:
                        channel_count: 1
                        bus: Control.kr[3:in_]
                -   BinaryOpUGen(MULTIPLICATION).ar:
                        left: InFeedback.ar[0]
                        right: EnvGen.kr[0]
                -   Out.ar:
                        bus: Control.kr[4:out]
                        source[0]: BinaryOpUGen(MULTIPLICATION).ar[0]
            """,
        ),
        (
            system_link_audio_2,
            """
            synthdef:
                name: supriya:link-ar:2
                ugens:
                -   Control.kr:
                        done_action: 2.0
                        fade_time: 0.02
                        gate: 1.0
                        in_: 16.0
                        out: 0.0
                -   BinaryOpUGen(LESS_THAN_OR_EQUAL).kr:
                        left: Control.kr[1:fade_time]
                        right: 0.0
                -   EnvGen.kr:
                        gate: Control.kr[2:gate]
                        level_scale: 1.0
                        level_bias: 0.0
                        time_scale: Control.kr[1:fade_time]
                        done_action: Control.kr[0:done_action]
                        envelope[0]: BinaryOpUGen(LESS_THAN_OR_EQUAL).kr[0]
                        envelope[1]: 2.0
                        envelope[2]: 1.0
                        envelope[3]: -99.0
                        envelope[4]: 1.0
                        envelope[5]: 1.0
                        envelope[6]: 3.0
                        envelope[7]: 0.0
                        envelope[8]: 0.0
                        envelope[9]: 1.0
                        envelope[10]: 3.0
                        envelope[11]: 0.0
                -   InFeedback.ar:
                        channel_count: 2
                        bus: Control.kr[3:in_]
                -   BinaryOpUGen(MULTIPLICATION).ar/0:
                        left: InFeedback.ar[0]
                        right: EnvGen.kr[0]
                -   BinaryOpUGen(MULTIPLICATION).ar/1:
                        left: InFeedback.ar[1]
                        right: EnvGen.kr[0]
                -   Out.ar:
                        bus: Control.kr[4:out]
                        source[0]: BinaryOpUGen(MULTIPLICATION).ar/0[0]
                        source[1]: BinaryOpUGen(MULTIPLICATION).ar/1[0]
            """,
        ),
        (
            amplitude_scope_audio_1,
            """
            synthdef:
                name: supriya:amp-scope-ar:1
                ugens:
                -   Control.kr:
                        in_: 0.0
                        max_frames: 4096.0
                        scope_frames: 4096.0
                        scope_id: 0.0
                -   In.ar:
                        channel_count: 1
                        bus: Control.kr[0:in_]
                -   ScopeOut2.ar:
                        scope_id: Control.kr[3:scope_id]
                        max_frames: Control.kr[1:max_frames]
                        scope_frames: Control.kr[2:scope_frames]
                        source[0]: In.ar[0]
            """,
        ),
        (
            amplitude_scope_control_2,
            """
            synthdef:
                name: supriya:amp-scope-kr:2
                ugens:
                -   Control.kr:
                        in_: 0.0
                        max_frames: 4096.0
                        scope_frames: 4096.0
                        scope_id: 0.0
                -   In.kr:
                        channel_count: 2
                        bus: Control.kr[0:in_]
                -   K2A.ar/0:
                        source: In.kr[0]
                -   K2A.ar/1:
                        source: In.kr[1]
                -   ScopeOut2.ar:
                        scope_id: Control.kr[3:scope_id]
                        max_frames: Control.kr[1:max_frames]
                        scope_frames: Control.kr[2:scope_frames]
                        source[0]: K2A.ar/0[0]
                        source[1]: K2A.ar/1[0]
            """,
        ),
        (
            frequency_scope_lin_1,
            """
            synthdef:
                name: supriya:freq-scope-lin:1
                ugens:
                -   Control.ir:
                        fft_buffer_size: 2048.0
                        rate: 4.0
                        scope_id: 0.0
                -   UnaryOpUGen(RECIPROCAL).ir:
                        source: Control.ir[0:fft_buffer_size]
                -   BinaryOpUGen(MULTIPLICATION).ir/0:
                        left: Control.ir[1:rate]
                        right: UnaryOpUGen(RECIPROCAL).ir[0]
                -   BinaryOpUGen(SUBTRACTION).ir:
                        left: 1.0
                        right: BinaryOpUGen(MULTIPLICATION).ir/0[0]
                -   Control.kr:
                        in_: 0.0
                -   MaxLocalBufs.ir:
                        maximum: 1.0
                -   LocalBuf.ir:
                        channel_count: 1.0
                        frame_count: Control.ir[0:fft_buffer_size]
                -   BufSamples.ir:
                        buffer_id: LocalBuf.ir[0]
                -   BinaryOpUGen(MULTIPLICATION).ir/1:
                        left: BufSamples.ir[0]
                        right: 0.5
                -   In.ar:
                        channel_count: 1
                        bus: Control.kr[0:in_]
                -   FFT.kr:
                        buffer_id: LocalBuf.ir[0]
                        source: In.ar[0]
                        hop: 0.75
                        window_type: 1.0
                        active: 1.0
                        window_size: 0.0
                -   PV_MagSmear.kr:
                        pv_chain: FFT.kr[0]
                        bins: 1.0
                -   BufDur.ir:
                        buffer_id: LocalBuf.ir[0]
                -   BinaryOpUGen(FLOAT_DIVISION).ir:
                        left: Control.ir[1:rate]
                        right: BufDur.ir[0]
                -   LFSaw.ar:
                        frequency: BinaryOpUGen(FLOAT_DIVISION).ir[0]
                        initial_phase: BinaryOpUGen(SUBTRACTION).ir[0]
                -   MulAdd.ar:
                        source: LFSaw.ar[0]
                        multiplier: BinaryOpUGen(MULTIPLICATION).ir/1[0]
                        addend: BinaryOpUGen(MULTIPLICATION).ir/1[0]
                -   BinaryOpUGen(ROUND).ar:
                        left: MulAdd.ar[0]
                        right: 2.0
                -   BufRd.ar:
                        channel_count: 1
                        buffer_id: LocalBuf.ir[0]
                        phase: BinaryOpUGen(ROUND).ar[0]
                        loop: 1.0
                        interpolation: 1.0
                -   BinaryOpUGen(FLOAT_DIVISION).ar:
                        left: BufRd.ar[0]
                        right: Control.ir[0:fft_buffer_size]
                -   UnaryOpUGen(AMPLITUDE_TO_DB).ar:
                        source: BinaryOpUGen(FLOAT_DIVISION).ar[0]
                -   ScopeOut.ar:
                        buffer_id: Control.ir[2:scope_id]
                        source[0]: UnaryOpUGen(AMPLITUDE_TO_DB).ar[0]
            """,
        ),
        (
            frequency_scope_log_1,
            """
            synthdef:
                name: supriya:freq-scope-log:1
                ugens:
                -   Control.ir:
                        fft_buffer_size: 2048.0
                        rate: 4.0
                        scope_id: 0.0
                -   UnaryOpUGen(RECIPROCAL).ir:
                        source: Control.ir[0:fft_buffer_size]
                -   BinaryOpUGen(MULTIPLICATION).ir/0:
                        left: Control.ir[1:rate]
                        right: UnaryOpUGen(RECIPROCAL).ir[0]
                -   BinaryOpUGen(SUBTRACTION).ir:
                        left: 1.0
                        right: BinaryOpUGen(MULTIPLICATION).ir/0[0]
                -   Control.kr:
                        in_: 0.0
                -   MaxLocalBufs.ir:
                        maximum: 1.0
                -   LocalBuf.ir:
                        channel_count: 1.0
                        frame_count: Control.ir[0:fft_buffer_size]
                -   BufSamples.ir:
                        buffer_id: LocalBuf.ir[0]
                -   BinaryOpUGen(MULTIPLICATION).ir/1:
                        left: BufSamples.ir[0]
                        right: 0.5
                -   In.ar:
                        channel_count: 1
                        bus: Control.kr[0:in_]
                -   FFT.kr:
                        buffer_id: LocalBuf.ir[0]
                        source: In.ar[0]
                        hop: 0.75
                        window_type: 1.0
                        active: 1.0
                        window_size: 0.0
                -   PV_MagSmear.kr:
                        pv_chain: FFT.kr[0]
                        bins: 1.0
                -   BufDur.ir:
                        buffer_id: LocalBuf.ir[0]
                -   BinaryOpUGen(FLOAT_DIVISION).ir:
                        left: Control.ir[1:rate]
                        right: BufDur.ir[0]
                -   LFSaw.ar:
                        frequency: BinaryOpUGen(FLOAT_DIVISION).ir[0]
                        initial_phase: BinaryOpUGen(SUBTRACTION).ir[0]
                -   MulAdd.ar:
                        source: LFSaw.ar[0]
                        multiplier: 0.5
                        addend: 0.5
                -   BinaryOpUGen(POWER).ar:
                        left: BinaryOpUGen(MULTIPLICATION).ir/1[0]
                        right: MulAdd.ar[0]
                -   BinaryOpUGen(MULTIPLICATION).ar:
                        left: BinaryOpUGen(POWER).ar[0]
                        right: 2.0
                -   BinaryOpUGen(ROUND).ar:
                        left: BinaryOpUGen(MULTIPLICATION).ar[0]
                        right: 2.0
                -   BufRd.ar:
                        channel_count: 1
                        buffer_id: LocalBuf.ir[0]
                        phase: BinaryOpUGen(ROUND).ar[0]
                        loop: 1.0
                        interpolation: 1.0
                -   BinaryOpUGen(FLOAT_DIVISION).ar:
                        left: BufRd.ar[0]
                        right: Control.ir[0:fft_buffer_size]
                -   UnaryOpUGen(AMPLITUDE_TO_DB).ar:
                        source: BinaryOpUGen(FLOAT_DIVISION).ar[0]
                -   ScopeOut.ar:
                        buffer_id: Control.ir[2:scope_id]
                        source[0]: UnaryOpUGen(AMPLITUDE_TO_DB).ar[0]
            """,
        ),
        (
            frequency_scope_lin_shm_1,
            """
            synthdef:
                name: supriya:freq-scope-lin-shm:1
                ugens:
                -   Control.ir:
                        fft_buffer_size: 2048.0
                        rate: 4.0
                        scope_id: 0.0
                -   UnaryOpUGen(RECIPROCAL).ir:
                        source: Control.ir[0:fft_buffer_size]
                -   BinaryOpUGen(MULTIPLICATION).ir/0:
                        left: Control.ir[1:rate]
                        right: UnaryOpUGen(RECIPROCAL).ir[0]
                -   BinaryOpUGen(SUBTRACTION).ir:
                        left: 1.0
                        right: BinaryOpUGen(MULTIPLICATION).ir/0[0]
                -   Control.kr:
                        in_: 0.0
                -   MaxLocalBufs.ir:
                        maximum: 1.0
                -   LocalBuf.ir:
                        channel_count: 1.0
                        frame_count: Control.ir[0:fft_buffer_size]
                -   BufSamples.ir:
                        buffer_id: LocalBuf.ir[0]
                -   BinaryOpUGen(MULTIPLICATION).ir/1:
                        left: BufSamples.ir[0]
                        right: 0.5
                -   In.ar:
                        channel_count: 1
                        bus: Control.kr[0:in_]
                -   FFT.kr:
                        buffer_id: LocalBuf.ir[0]
                        source: In.ar[0]
                        hop: 0.75
                        window_type: 1.0
                        active: 1.0
                        window_size: 0.0
                -   PV_MagSmear.kr:
                        pv_chain: FFT.kr[0]
                        bins: 1.0
                -   BufDur.ir:
                        buffer_id: LocalBuf.ir[0]
                -   BinaryOpUGen(FLOAT_DIVISION).ir/0:
                        left: Control.ir[1:rate]
                        right: BufDur.ir[0]
                -   LFSaw.ar:
                        frequency: BinaryOpUGen(FLOAT_DIVISION).ir/0[0]
                        initial_phase: BinaryOpUGen(SUBTRACTION).ir[0]
                -   MulAdd.ar:
                        source: LFSaw.ar[0]
                        multiplier: BinaryOpUGen(MULTIPLICATION).ir/1[0]
                        addend: BinaryOpUGen(MULTIPLICATION).ir/1[0]
                -   BinaryOpUGen(ROUND).ar:
                        left: MulAdd.ar[0]
                        right: 2.0
                -   BufRd.ar:
                        channel_count: 1
                        buffer_id: LocalBuf.ir[0]
                        phase: BinaryOpUGen(ROUND).ar[0]
                        loop: 1.0
                        interpolation: 1.0
                -   BinaryOpUGen(FLOAT_DIVISION).ar:
                        left: BufRd.ar[0]
                        right: Control.ir[0:fft_buffer_size]
                -   UnaryOpUGen(AMPLITUDE_TO_DB).ar:
                        source: BinaryOpUGen(FLOAT_DIVISION).ar[0]
                -   BinaryOpUGen(FLOAT_DIVISION).ir/1:
                        left: Control.ir[0:fft_buffer_size]
                        right: Control.ir[1:rate]
                -   ScopeOut2.ar:
                        scope_id: Control.ir[2:scope_id]
                        max_frames: BinaryOpUGen(FLOAT_DIVISION).ir/1[0]
                        scope_frames: BinaryOpUGen(FLOAT_DIVISION).ir/1[0]
                        source[0]: UnaryOpUGen(AMPLITUDE_TO_DB).ar[0]
            """,
        ),
        (
            frequency_scope_log_shm_2,
            """
            synthdef:
                name: supriya:freq-scope-log-shm:2
                ugens:
                -   Control.ir:
                        fft_buffer_size: 2048.0
                        rate: 4.0
                        scope_id: 0.0
                -   UnaryOpUGen(RECIPROCAL).ir:
                        source: Control.ir[0:fft_buffer_size]
                -   BinaryOpUGen(MULTIPLICATION).ir/0:
                        left: Control.ir[1:rate]
                        right: UnaryOpUGen(RECIPROCAL).ir[0]
                -   BinaryOpUGen(SUBTRACTION).ir:
                        left: 1.0
                        right: BinaryOpUGen(MULTIPLICATION).ir/0[0]
                -   Control.kr:
                        in_: 0.0
                -   MaxLocalBufs.ir:
                        maximum: 1.0
                -   LocalBuf.ir:
                        channel_count: 1.0
                        frame_count: Control.ir[0:fft_buffer_size]
                -   BufSamples.ir:
                        buffer_id: LocalBuf.ir[0]
                -   BinaryOpUGen(MULTIPLICATION).ir/1:
                        left: BufSamples.ir[0]
                        right: 0.5
                -   In.ar:
                        channel_count: 1
                        bus: Control.kr[0:in_]
                -   FFT.kr:
                        buffer_id: LocalBuf.ir[0]
                        source: In.ar[0]
                        hop: 0.75
                        window_type: 1.0
                        active: 1.0
                        window_size: 0.0
                -   PV_MagSmear.kr:
                        pv_chain: FFT.kr[0]
                        bins: 1.0
                -   BufDur.ir:
                        buffer_id: LocalBuf.ir[0]
                -   BinaryOpUGen(FLOAT_DIVISION).ir/0:
                        left: Control.ir[1:rate]
                        right: BufDur.ir[0]
                -   LFSaw.ar:
                        frequency: BinaryOpUGen(FLOAT_DIVISION).ir/0[0]
                        initial_phase: BinaryOpUGen(SUBTRACTION).ir[0]
                -   MulAdd.ar:
                        source: LFSaw.ar[0]
                        multiplier: 0.5
                        addend: 0.5
                -   BinaryOpUGen(POWER).ar:
                        left: BinaryOpUGen(MULTIPLICATION).ir/1[0]
                        right: MulAdd.ar[0]
                -   BinaryOpUGen(MULTIPLICATION).ar:
                        left: BinaryOpUGen(POWER).ar[0]
                        right: 2.0
                -   BinaryOpUGen(ROUND).ar:
                        left: BinaryOpUGen(MULTIPLICATION).ar[0]
                        right: 2.0
                -   BufRd.ar:
                        channel_count: 1
                        buffer_id: LocalBuf.ir[0]
                        phase: BinaryOpUGen(ROUND).ar[0]
                        loop: 1.0
                        interpolation: 1.0
                -   BinaryOpUGen(FLOAT_DIVISION).ar:
                        left: BufRd.ar[0]
                        right: Control.ir[0:fft_buffer_size]
                -   UnaryOpUGen(AMPLITUDE_TO_DB).ar:
                        source: BinaryOpUGen(FLOAT_DIVISION).ar[0]
                -   BinaryOpUGen(FLOAT_DIVISION).ir/1:
                        left: Control.ir[0:fft_buffer_size]
                        right: Control.ir[1:rate]
                -   ScopeOut2.ar:
                        scope_id: Control.ir[2:scope_id]
                        max_frames: BinaryOpUGen(FLOAT_DIVISION).ir/1[0]
                        scope_frames: BinaryOpUGen(FLOAT_DIVISION).ir/1[0]
                        source[0]: UnaryOpUGen(AMPLITUDE_TO_DB).ar[0]
            """,
        ),
    ],
)
def test_supriya(
    synthdef: SynthDef,
    expected_str: str,
) -> None:
    assert normalize(str(synthdef)) == normalize(expected_str)


@pytest.mark.parametrize(
    "sclang_name, sclang_body, sclang_rates, expected_str",
    [
        (
            "system_link_audio_1",
            r"""
            | out=0, in=16, vol=1, level=1, lag=0.05, doneAction=2 |
            var env = EnvGate(i_level: 0, doneAction:doneAction, curve:'sin')
            * Lag.kr(vol * level, lag);
            Out.ar(out, InFeedback.ar(in, 1) * env)
            """,
            r"[\kr, \kr, \kr, \kr, \kr, \ir]",
            """
            synthdef:
                name: system_link_audio_1
                ugens:
                -   Control.ir:
                        doneAction: 2.0
                -   Control.kr:
                        out: 0.0
                        in: 16.0
                        vol: 1.0
                        level: 1.0
                        lag: 0.05000000074505806
                -   BinaryOpUGen(MULTIPLICATION).kr/0:
                        left: Control.kr[2:vol]
                        right: Control.kr[3:level]
                -   Lag.kr:
                        source: BinaryOpUGen(MULTIPLICATION).kr/0[0]
                        lag_time: Control.kr[4:lag]
                -   InFeedback.ar:
                        channel_count: 1
                        bus: Control.kr[1:in]
                -   Control.kr:
                        gate: 1.0
                -   Control.kr:
                        fadeTime: 0.019999999552965164
                -   EnvGen.kr:
                        gate: Control.kr[0:gate]
                        level_scale: 1.0
                        level_bias: 0.0
                        time_scale: Control.kr[0:fadeTime]
                        done_action: Control.ir[0:doneAction]
                        envelope[0]: 0.0
                        envelope[1]: 2.0
                        envelope[2]: 1.0
                        envelope[3]: -99.0
                        envelope[4]: 1.0
                        envelope[5]: 1.0
                        envelope[6]: 3.0
                        envelope[7]: 0.0
                        envelope[8]: 0.0
                        envelope[9]: 1.0
                        envelope[10]: 3.0
                        envelope[11]: 0.0
                -   BinaryOpUGen(MULTIPLICATION).kr/1:
                        left: EnvGen.kr[0]
                        right: Lag.kr[0]
                -   BinaryOpUGen(MULTIPLICATION).ar:
                        left: InFeedback.ar[0]
                        right: BinaryOpUGen(MULTIPLICATION).kr/1[0]
                -   Out.ar:
                        bus: Control.kr[0:out]
                        source[0]: BinaryOpUGen(MULTIPLICATION).ar[0]
            """,
        ),
        (
            "system_link_audio_2",
            r"""
            | out=0, in=16, vol=1, level=1, lag=0.05, doneAction=2 |
            var env = EnvGate(i_level: 0, doneAction:doneAction, curve:'sin')
            * Lag.kr(vol * level, lag);
            Out.ar(out, InFeedback.ar(in, 2) * env)
            """,
            r"[\kr, \kr, \kr, \kr, \kr, \ir]",
            """
            synthdef:
                name: system_link_audio_2
                ugens:
                -   Control.ir:
                        doneAction: 2.0
                -   Control.kr:
                        out: 0.0
                        in: 16.0
                        vol: 1.0
                        level: 1.0
                        lag: 0.05000000074505806
                -   BinaryOpUGen(MULTIPLICATION).kr/0:
                        left: Control.kr[2:vol]
                        right: Control.kr[3:level]
                -   Lag.kr:
                        source: BinaryOpUGen(MULTIPLICATION).kr/0[0]
                        lag_time: Control.kr[4:lag]
                -   InFeedback.ar:
                        channel_count: 2
                        bus: Control.kr[1:in]
                -   Control.kr:
                        gate: 1.0
                -   Control.kr:
                        fadeTime: 0.019999999552965164
                -   EnvGen.kr:
                        gate: Control.kr[0:gate]
                        level_scale: 1.0
                        level_bias: 0.0
                        time_scale: Control.kr[0:fadeTime]
                        done_action: Control.ir[0:doneAction]
                        envelope[0]: 0.0
                        envelope[1]: 2.0
                        envelope[2]: 1.0
                        envelope[3]: -99.0
                        envelope[4]: 1.0
                        envelope[5]: 1.0
                        envelope[6]: 3.0
                        envelope[7]: 0.0
                        envelope[8]: 0.0
                        envelope[9]: 1.0
                        envelope[10]: 3.0
                        envelope[11]: 0.0
                -   BinaryOpUGen(MULTIPLICATION).kr/1:
                        left: EnvGen.kr[0]
                        right: Lag.kr[0]
                -   BinaryOpUGen(MULTIPLICATION).ar/0:
                        left: InFeedback.ar[0]
                        right: BinaryOpUGen(MULTIPLICATION).kr/1[0]
                -   BinaryOpUGen(MULTIPLICATION).ar/1:
                        left: InFeedback.ar[1]
                        right: BinaryOpUGen(MULTIPLICATION).kr/1[0]
                -   Out.ar:
                        bus: Control.kr[0:out]
                        source[0]: BinaryOpUGen(MULTIPLICATION).ar/0[0]
                        source[1]: BinaryOpUGen(MULTIPLICATION).ar/1[0]
            """,
        ),
        (
            "system_freqScope0_shm",
            r"""
            arg in=0, fftBufSize = 2048, scopebufnum=1, rate=4, dbFactor = 0.02;
			var phase = 1 - (rate * fftBufSize.reciprocal);
			var signal, chain, phasor, numSamples, mul;
			var fftbufnum = LocalBuf(fftBufSize, 1);
			mul = 0.00285;
			numSamples = (BufSamples.ir(fftbufnum) - 2) * 0.5; // 1023 (bufsize=2048)
			signal = In.ar(in);
			chain = FFT(fftbufnum, signal, hop: 0.75, wintype:1);
			chain = PV_MagSmear(chain, 1);
			// -1023 to 1023, 0 to 2046, 2 to 2048 (skip first 2 elements DC and Nyquist)
			phasor = LFSaw.ar(rate/BufDur.ir(fftbufnum), phase, numSamples, numSamples + 2);
			phasor = phasor.round(2); // the evens are magnitude
			ScopeOut2.ar(
				((BufRd.ar(1, fftbufnum, phasor, 1, 1) * mul).ampdb * dbFactor) + 1,
				scopebufnum,
				fftBufSize/rate
			);
            """,
            r"[\kr, \ir, \ir, \ir, \kr]",
            """
            synthdef:
                name: system_freqScope0_shm
                ugens:
                -   Control.ir:
                        fftBufSize: 2048.0
                        scopebufnum: 1.0
                        rate: 4.0
                -   UnaryOpUGen(RECIPROCAL).ir:
                        source: Control.ir[0:fftBufSize]
                -   BinaryOpUGen(MULTIPLICATION).ir/0:
                        left: Control.ir[2:rate]
                        right: UnaryOpUGen(RECIPROCAL).ir[0]
                -   BinaryOpUGen(SUBTRACTION).ir/0:
                        left: 1.0
                        right: BinaryOpUGen(MULTIPLICATION).ir/0[0]
                -   Control.kr:
                        in: 0.0
                        dbFactor: 0.019999999552965164
                -   MaxLocalBufs.ir:
                        maximum: 1.0
                -   LocalBuf.ir:
                        channel_count: 1.0
                        frame_count: Control.ir[0:fftBufSize]
                -   BufSamples.ir:
                        buffer_id: LocalBuf.ir[0]
                -   BinaryOpUGen(SUBTRACTION).ir/1:
                        left: BufSamples.ir[0]
                        right: 2.0
                -   BinaryOpUGen(MULTIPLICATION).ir/1:
                        left: BinaryOpUGen(SUBTRACTION).ir/1[0]
                        right: 0.5
                -   In.ar:
                        channel_count: 1
                        bus: Control.kr[0:in]
                -   FFT.kr:
                        buffer_id: LocalBuf.ir[0]
                        source: In.ar[0]
                        hop: 0.75
                        window_type: 1.0
                        active: 1.0
                        window_size: 0.0
                -   PV_MagSmear.kr:
                        pv_chain: FFT.kr[0]
                        bins: 1.0
                -   BufDur.ir:
                        buffer_id: LocalBuf.ir[0]
                -   BinaryOpUGen(FLOAT_DIVISION).ir/0:
                        left: Control.ir[2:rate]
                        right: BufDur.ir[0]
                -   LFSaw.ar:
                        frequency: BinaryOpUGen(FLOAT_DIVISION).ir/0[0]
                        initial_phase: BinaryOpUGen(SUBTRACTION).ir/0[0]
                -   BinaryOpUGen(ADDITION).ir:
                        left: BinaryOpUGen(MULTIPLICATION).ir/1[0]
                        right: 2.0
                -   MulAdd.ar/0:
                        source: LFSaw.ar[0]
                        multiplier: BinaryOpUGen(MULTIPLICATION).ir/1[0]
                        addend: BinaryOpUGen(ADDITION).ir[0]
                -   BinaryOpUGen(ROUND).ar:
                        left: MulAdd.ar/0[0]
                        right: 2.0
                -   BufRd.ar:
                        channel_count: 1
                        buffer_id: LocalBuf.ir[0]
                        phase: BinaryOpUGen(ROUND).ar[0]
                        loop: 1.0
                        interpolation: 1.0
                -   BinaryOpUGen(MULTIPLICATION).ar:
                        left: BufRd.ar[0]
                        right: 0.002850000048056245
                -   UnaryOpUGen(AMPLITUDE_TO_DB).ar:
                        source: BinaryOpUGen(MULTIPLICATION).ar[0]
                -   MulAdd.ar/1:
                        source: UnaryOpUGen(AMPLITUDE_TO_DB).ar[0]
                        multiplier: Control.kr[1:dbFactor]
                        addend: 1.0
                -   BinaryOpUGen(FLOAT_DIVISION).ir/1:
                        left: Control.ir[0:fftBufSize]
                        right: Control.ir[2:rate]
                -   ScopeOut2.ar:
                        scope_id: Control.ir[1:scopebufnum]
                        max_frames: BinaryOpUGen(FLOAT_DIVISION).ir/1[0]
                        scope_frames: BinaryOpUGen(FLOAT_DIVISION).ir/1[0]
                        source[0]: MulAdd.ar/1[0]
            """,
        ),
    ],
)
@pytest.mark.skipif(platform.system() == "Windows", reason="hangs on Windows")
@pytest.mark.skipif(
    platform.system() == "Darwin" and os.environ.get("CI") == "true",
    reason="sclang hangs without QT",
)
def test_sclang(
    sclang_name: str, sclang_body: str, sclang_rates: str, expected_str: str
) -> None:
    compiled = SuperColliderSynthDef(sclang_name, sclang_body, sclang_rates).compile()
    synthdef = decompile_synthdef(compiled)
    assert normalize(str(synthdef)) == normalize(expected_str)
