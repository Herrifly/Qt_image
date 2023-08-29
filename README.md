# Qt_image

## Prepare project environment
~~~bash
mkdir ~/points_image
git clone git@github.com:Uni-Schedule-App/backend.git backend
python3 -m venv venv
source venv/bin/activate && cd ~/uni-app/backend
pip install -r  requirements.txt
~~~

Функционал ПО:
  1) Открытие изображения из проводника.
  2) Двойным кликом мыши выделение точек интереса (они будут отображаться красным эллипсом на картинке)
  3) Есть зум, который меняется колесиком мыши, при зуме больше 1, координаты точки интереса сохраняются с точностью до десятых.
  4) При желании очистить выделенные точки, есть кнопка "Очистить точки".
