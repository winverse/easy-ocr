# PDF to text

super easy pdf to text for korean using [tesseract-ocr](https://github.com/tesseract-ocr/tesseract) with docker


# run
Open your terminal and run below command (needs docker)
```sh
  ./scripts/build.sh
  ./scripts/run.sh
```

# Open docs 
After run docker container, enter the link your browser.  
http://localhost:5001/docs or http://localhost:5001/redoc


# Stop and Remove container & image

```sh
  ./scripts/rm.sh
```