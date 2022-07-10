## 개발 환경

python : 3.9.6

django : 4.0.6

## 개발 환경 설정
```
python -m venv testapivenv

EXCUTE testapivenv/Scripts/activate

pip install django djangorestframework

python -m pip install --upgrade pip 
```
## 장고 프로젝트 생성
```
mkdir testapi

cd testapi

django-admin startproject config .
```
config/settings.py 에서 해당 내용 작성(한국어, 한국 시간 적용)

```python
LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = False
```

## migrate makemigrations content
```
python manage.py makemigrations

python manage.py migrate
```

## API Explanation
```
/patient : patient data CRUD

/doctor/info : doctor data CRUD

/doctor/etc : data related to doctor CRUD

/treatmentrequest : treatmentrequest data CRUD
```
