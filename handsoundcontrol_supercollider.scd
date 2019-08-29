//  SERVER Initalization

s.boot

// SYNTH Initalization
(
SynthDef(\hihat, {arg out = 0, amp = 0.1, att = 0.01, rel = 0.2, ffreq = 6000, pan = 0;
	var env, snd;
	env = Env.perc(att, rel, amp).kr(doneAction: 2);
	snd = WhiteNoise.ar;
	snd = HPF.ar(in: snd, freq: ffreq, mul: env);
	Out.ar(out, Pan2.ar(snd, pan));

}).add;

SynthDef(\snare, {arg out = 0, amp = 0.1, sinfreq = 180, att = 0.01, rel = 0.2, ffreq = 2000, pan = 0;
	var env, snd1, snd2, sum;
	env = Env.perc(att, rel, amp).kr(doneAction: 2);
	snd1 = HPF.ar(
		in: WhiteNoise.ar,
		freq: ffreq,
		mul: env
	);
	snd2 = SinOsc.ar(freq: sinfreq, mul: env);
	sum = snd1 + snd2;
	Out.ar(out, Pan2.ar(sum, pan));

}).add;

SynthDef(\kick, {arg out = 0, amp = 0.6, sinfreq = 60, glissf = 0.9, att = 0.01, rel = 0.45, pan = 0;
	var env, snd, ramp;
	env = Env.perc(att, rel, amp).kr(doneAction: 2);
	ramp = XLine.kr(
		start: sinfreq,
		end: sinfreq * glissf,
		dur: rel
	);
	snd = SinOsc.ar(freq: ramp, mul: env);
	snd = Pan2.ar(snd, pan);
	Out.ar(out, snd);

}).add;

SynthDef(\Piano_rhodeySC, {
	//FM Rhodes Synthethizer
    |
    // standard meanings
    out = 0, freq = 440, gate = 1, pan = 0, amp = 0.05,
    // all of these range from 0 to 1
    vel = 0.8, modIndex = 0.2, mix = 0.2, lfoSpeed = 0.4, lfoDepth = 0.1
    |
    var env1, env2, env3, env4;
    var osc1, osc2, osc3, osc4, snd;

    lfoSpeed = lfoSpeed * 12;

    freq = freq * 2;

    env1 = EnvGen.ar(Env.adsr(0.001, 1.25, 0.0, 0.04, curve: \lin));
    env2 = EnvGen.ar(Env.adsr(0.001, 1.00, 0.0, 0.04, curve: \lin));
    env3 = EnvGen.ar(Env.adsr(0.001, 1.50, 0.0, 0.04, curve: \lin));
    env4 = EnvGen.ar(Env.adsr(0.001, 1.50, 0.0, 0.04, curve: \lin));

    osc4 = SinOsc.ar(freq * 0.5) * 2pi * 2 * 0.535887 * modIndex * env4 * vel;
    osc3 = SinOsc.ar(freq, osc4) * env3 * vel;
    osc2 = SinOsc.ar(freq * 15) * 2pi * 0.108819 * env2 * vel;
    osc1 = SinOsc.ar(freq, osc2) * env1 * vel;
    snd = Mix((osc3 * (1 - mix)) + (osc1 * mix));
    snd = snd * (SinOsc.ar(lfoSpeed) * lfoDepth + 1);

    // using the doneAction: 2 on the other envs can create clicks (bc of the linear curve maybe?)
    snd = snd * EnvGen.ar(Env.asr(0, 1, 0.1), gate, doneAction: 2);
    snd = Pan2.ar(snd, pan, amp);

    Out.ar(out, snd);
}).add;


SynthDef( \klanks, { arg freqScale = 1.0, amp = 0.1;
	var trig, klan;
	var  p, exc, x, s;
	trig = Impulse.ar( 0 );
	klan = Klank.ar(`[ Array.fill( 16, { linrand(8000.0 ) + 60 }), nil, Array.fill( 16, { rrand( 0.1, 2.0)})], trig, freqScale );
	klan = (klan * amp).softclip;
	DetectSilence.ar( klan, doneAction: 2 );
	Out.ar( 0, Pan2.ar( klan ));
}).add;

SynthDef(\marimba, {arg freq = 440, amp = 0.1;
	var snd, env;
	env = Env.linen(0.015, 1, 0.5, amp).kr(doneAction: 2);
	snd = BPF.ar(Saw.ar(0), freq, 0.02);
	snd = BLowShelf.ar(snd, 220, 0.81, 6);
	snd = snd * env;
	Out.ar(0, Splay.ar(snd));
}).add;

)



//COMMUNICATION initalization

NetAddr("127.0.0.1",57120);

// TEMPO CLOCK initalization

t = TempoClock(4);


//---------------- Tempo Function --------------

(

OSCdef('OSCreceiver',
	{
		arg msg;
		msg[1].postln;
		msg[2].postln;


		if (msg[1]==200, {

			t.clear });




		if (msg[1]==66, {
t.schedAbs(t.beats.ceil+(4-t.beats.ceil%4), {arg beat, sec;
	        t.clear;
	        t.beats=beat+(6-beat%6);
			//t.beats.postln;

			t.schedAbs((t.beats.ceil+(6-t.beats.ceil%6)), { arg beat, sec;
		    // "beat : ".post; beat.postln;
			if (beat % 6==3, {Synth(\snare)});
			if (beat % 1==0, {Synth(\hihat)});
			if (beat % 6==0, {Synth(\kick)});
				1 // 1 here means that we are repeating/looping this
			});
		}); });



		if (msg[1]==44, {
t.schedAbs(t.beats.ceil+(6-t.beats.ceil%6), {
	        t.clear;
	        t.beats=t.beats.ceil+(4-t.beats.ceil%4);


			t.schedAbs(t.beats.ceil+(4-t.beats.ceil%4), { arg beat, sec;
				//"beat : ".post; beat.postln;
				if (beat % 4==2, {Synth(\snare)});
				if (beat % 1==0, {Synth(\hihat)});
				if (beat % 4==0, {Synth(\kick)});
				1 // 1 here means that we are repeating/looping this
			});
		}); });

//---------------- Synth Function --------------

        if (msg[1]==101, {
		t.schedAbs(t.beats.ceil, { arg beat, sec;

			if (beat % 4==0, {Synth(\marimba, [\freq, 67.midicps])});
			if (beat % 4==2, {Synth(\marimba, [\freq, 60.midicps])});
			if ((beat % 4==1) || (beat % 4==3), {Synth(\marimba, [\freq, 48.midicps])});
			1; // repeat
		});  });


		   if (msg[1]==100, {
		t.schedAbs(t.beats.ceil, { arg beat, sec;

				if (beat % 7==0, {Synth(\marimba, [\freq, 67.midicps])});
				if (beat % 7==3, {Synth(\marimba, [\freq, 60.midicps])});
				if (beat % 7==5, {Synth(\marimba, [\freq, 48.midicps])});
			1; // repeat
		});  });


		if (msg[1]!=500 && msg[1]!='nil',

			{
				if (((msg[2]>325) && (msg[2]<450) && (msg[3]>10) && (msg[3]<125)),{

				t.play({Synth(\Piano_rhodeySC,[\freq,48.midicps]);
						Synth(\Piano_rhodeySC,[\freq,36.midicps]); });});

				if (((msg[2]>451) && (msg[2]<575) && (msg[3]>10) && (msg[3]<125)),{

				t.play({Synth(\Piano_rhodeySC,[\freq,37.midicps]);
						Synth(\Piano_rhodeySC,[\freq,49.midicps]); });});

				if (((msg[2]>325) && (msg[2]<450) && (msg[3]>126) && (msg[3]<240)),{

				t.play({Synth(\Piano_rhodeySC,[\freq,40.midicps]);
						Synth(\Piano_rhodeySC,[\freq,52.midicps]); });});

				if (((msg[2]>451) && (msg[2]<575) && (msg[3]>126) && (msg[3]<240)),{

			    t.play({Synth(\Piano_rhodeySC,[\freq,41.midicps]);
						Synth(\Piano_rhodeySC,[\freq,53.midicps]); });});

		});




	},"/first");
)







