pip install -U pip
pip install -U xformers~=0.0.23 --index-url https://download.pytorch.org/whl/cu121
pip install -U sdkit~=2.0.15 tqdm~=4.66.1 realesrgan~=0.3.0

mkdir -p ./tmp/image
python image.py $CONFIGPATH $MATRIXMODEL $WIDTH $HEIGHT

mkdir -p ./out
python upscale.py $CONFIGPATH
if ["$UPSCALE" != "OFF"]; then
    UPSCALE_INT=$(echo "$UPSCALE" | awk '{print int($1)}')
    python ./tmp/inference_script.py -i ./tmp/image/1.jpg --model_path ./tmp/model.pth -o ./out/ --fp32 -s $UPSCALE_INT
    echo "Upscaled image!"
fi

mv ./out/*.jpg ./out/$RUNNUM-$JOBINDEX-$RUNID.jpg