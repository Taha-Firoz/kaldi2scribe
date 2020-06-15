import argparse
from os import path
from glob import glob
from kaldi.asr import GmmLatticeFasterRecognizer
from kaldi.decoder import LatticeFasterDecoderOptions
from kaldi.util.table import SequentialMatrixReader, SequentialWaveReader


ap = argparse.ArgumentParser(prog="kaldi2scribe", usage="%(prog)s --modelroot '/wsj/s5' --kaldiroot '/kaldi' --type 'tri1' --input '/transcription_test'", description='A quick and dirty way to transcribe audio with your trained Kaldi model')
ap.add_argument("-m", "--modelroot", required=True,
	help="root directory for the model")
ap.add_argument("-k", "--kaldiroot", required=True,
	help="root directory for kaldi")
ap.add_argument("-t", "--type", required=True,
	help="type of model: mono(Monophone model), tri1(Triphone Model + ∆), tri2a (tri1 + ∆), tri2b(tri1 + (LDA + MLLT)), tri3a(tri2b + MMI), tri3b(tri2b + Boosted MMI), tri3c(tri2b + MPE), tri3d(tri2b + SAT)")
ap.add_argument("-i", "--input", required=True,
	help="input directory to wav files")

args = vars(ap.parse_args())

AVAILABLE_MODEL_NAMES = ["mono", "tri1", "tri2","tri2a", "tri2b","tri3","tri3a", "tri3b", "tri3c", "tri3d"]
assert args["type"] in AVAILABLE_MODEL_NAMES, "The provided model name must be one of these:\n"+ AVAILABLE_MODEL_NAMES


def feat_pipeline(model_type):
    global KALDI_DIR, MODEL_ROOT, MODEL_DIR
    # define the rspecifier for reading the features
    compute_mfcc = f"{KALDI_DIR}/src/featbin/compute-mfcc-feats --allow-downsample --config={MODEL_ROOT}/conf/mfcc.conf scp:wav.scp ark:-"
    apply_cmvn = f"{KALDI_DIR}/src/featbin/apply-cmvn-sliding --cmn-window=1000000000 --center=true ark:- ark:-"
    add_deltas = f"{KALDI_DIR}/src/featbin/add-deltas ark:- ark:-"
    splice_feats = f"{KALDI_DIR}/src/featbin/splice-feats ark:- ark:-"
    transform_feats = f"{KALDI_DIR}/src/featbin/transform-feats {MODEL_DIR}/final.mat ark:- ark:-"

    if model_type in ["mono", "tri1", "tri2a"]:
            return f"ark,s,cs:{compute_mfcc} | {apply_cmvn} | {add_deltas} |"
    
    elif model_type in ["tri2","tri2b","tri3","tri3a", "tri3b", "tri3c", "tri3d"]:
            return f"ark,s,cs:{compute_mfcc} | {apply_cmvn} | {splice_feats} | {transform_feats} |"

def create_scp(data_path):
    assert path.exists(data_path), "Can't open folder"
    
    if path.isdir(data_path):
        wav_files = sorted(glob(path.join(data_path, "*.wav")))
        if len(wav_files) == 0:
            wav_files = sorted(glob(path.join(data_path, "*", "*.wav"), recursive=True))
    else:
        wav_files = [data_path]
    
    with open("wav.scp", "w") as fout:
        for wav_path in wav_files:
            _, wav_filename = path.split(wav_path)
            wav_filename = wav_filename[:-4] #remove extension
            fout.write("{} {}\n".format(wav_filename, wav_path))

#Generate scp file
create_scp(args["input"])

# Construct recognizer
decoder_opts = LatticeFasterDecoderOptions()
decoder_opts.beam = 13
decoder_opts.lattice_beam = 6.0
decoder_opts.max_active = 7000
        
KALDI_DIR = args["kaldiroot"]
TYPE = args["type"]
MODEL_ROOT = args["modelroot"]
MODEL_DIR = path.join(MODEL_ROOT, "exp", TYPE) 

asr = GmmLatticeFasterRecognizer\
        .from_files(
            path.join(MODEL_DIR, "final.mdl"),
            path.join(MODEL_DIR, "graph", "HCLG.fst"),
            path.join(MODEL_DIR, "graph", "words.txt"),
            decoder_opts=decoder_opts)

with SequentialMatrixReader(feat_pipeline(TYPE)) as f:
    for (key, feats) in f:
        out = asr.decode(feats)
        print(f"Audio file: {key}\nTrancription:",out["text"])
