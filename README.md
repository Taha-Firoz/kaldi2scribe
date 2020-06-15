# kaldi2scribe 

This repo represents weeks of frustration and difficulty I faced while trying to run my trained kaldi model. Yes, I know kaldi is a tool that was developed basically for researchers but in no way is it's undecipherable documentation justified.

Unless you have a really deep grasp of how Kaldi and ASR in general works you'll basically be getting no where. If you've been in a similar situation where you've followed the notorious [Kaldi for Dummies](https://kaldi-asr.org/doc/kaldi_for_dummies.html) tutorial and finally want to reap the fruits of your labour and see audio being transcribed, you'd be out of luck. It's as if no one from Kaldi's team every wondered if anyone would want to run their own models and actually see them transcribe text. You'll find resourced like [PyKaldi Examples](https://github.com/pykaldi/pykaldi/tree/master/examples) or [Nithing Rao's Medium article](https://medium.com/@nithinraok_/decoding-an-audio-file-using-a-pre-trained-model-with-kaldi-c1d7d2fe3dc5) but again for someone who's just following Kaldi for Dummies they probably won't understand how to get them to work. Also given that majority examples aren't for simple GMM setups but are based on running more complex TDNN or NN acoustic models, as a beginner you're going to have a hard time.

So I've made this small tool that takes in audio files, your model, and kaldi and spits out their transcriptions. I used [Anwarvic's](https://github.com/Anwarvic) really well written [Arabic-Speech-Recognition](https://github.com/Anwarvic/Arabic-Speech-Recognition/tree/master/Kaldi) repo to guide me through writing it. It is basically his work that I've gutted to just spit out transcriptions instead of evaluating your model's precision.

## Install
PyKaldi is available on conda, unless you plan on building it from scratch I'd highly recommend you use conda.
```
$ conda install --yes --file requirements.txt
```
You also need a copy of kaldi that's been built, if you've already trained a model then I guess you'll have a copy lying around. Just place the files this way:
```
kaldi2scribe.py
|
model root
└───exp
│   └───tri1
|   |   ...
kaldi root
└───nightmare fuel
|   |   ...
```
Tbh it doesn't really matter where everything is just make sure you `CWD` is at the same level as the Kaldi's root and yeah that's about it. 

## Usage
```
$ python3 kaldi2scribe.py --modelroot '/wsj/s5' --kaldiroot '/kaldi' --type 'tri1' --input '/transcription_test'
```
## Help
```
$ python3 kaldi2scribe.py -h
```
#### Note
This is a very basic tool just to help complete kaldi beginners to test their models, if you're looking at it for anything more then you're out of luck. If you have a better grasp on kaldi than I then make sure to contribute and know how to add support for more models don't hesistate to add a PR. 
