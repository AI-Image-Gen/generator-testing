pip install -U pip
pip install -U xformers --index-url https://download.pytorch.org/whl/cu121
pip install -U sdkit tqdm realesrgan

mkdir -p ./tmp/image
python image.py $CONFIGPATH $MATRIXMODEL $WIDTH $HEIGHT

mkdir -p ./out
python upscale.py $CONFIGPATH
python ./tmp/inference_script.py -i ./tmp/image/1.jpg --model_path ./tmp/model.pth -o ./out/ --fp32 -s $UPSCALE
echo "Upscaled image!"

mv ./out/*.jpg ./out/$RUNNUM-$JOBINDEX-$RUNID.jpg