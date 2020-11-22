# Automatically creates captions for images

It uses an attention-based model trained with the MS-COCO dataset.

### Use example:
```python
from image_to_text import img2txt_predict

img2txt_predict('https://tensorflow.org/images/surf.jpg')
#output: "a surfer riding on a wave"
```
