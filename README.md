# 더강사 프로그램 개발


### 개발환경 
- python platform : Anaconda3
- 개발언어 : python 3.7.6
- UI Design : PyQt 5.13.1
- Database : Mysql8.0.17  `Database name : jjtrading`
- OS : Windows10 Pro (x64)

### 증권사 API
- 키움증권 OpenAPI+


## 참고사항
#### windows 실행파일(.exe) 만드는 방법  : 
    `pyinstaller -w --add-data "resource;resource" --clean ./src/iredu_main.py`


#### Designer을 이용한 Form 수정하는 방법
    `C:\Python3.7\Lib\site-packages\pyqt5_tools\designer.exe` 를 이용하여 화면 수정


#### .UI 파일을 Python 코드로 변환 하는 방법 (pyuic 를 이용)
    `pyuic5 -x 소스파일명.ui -o 생성할파이썬파일명.py`
    `pyuic5 -x .\mw_main_view.ui -o ../src/view/form/mw_main_view.py`

### .qrc(리소스 파일)을 Python 코드로 변환하는 방법(pyrcc 를 이용)
    `pyrcc5 소스파일명.qrc -o 파이썬파일명.py`
    `pyrcc5 res_icons.qrc -o ../../src/view/form/res_icons_rc.py (리소스명에 _rc가 반드시 붙어야 한다.)`
    
### 명칭규칙 (PEP-8 규칙준수)
1. package 명 : 짧은 단어의 소문자. 언더스코어(_) 사용하지 않음.
1. module 명 : 짧은 단어의 소문자. (구분이 필요한 경우에 한하여 _ 사용 가능)
1. Functions(함수), Variables(변수), Attributes(속성)은 lowercase_underscore 형식을 따른다.
1. Protected instance attributes는 _leading_underscore 형식을 따른다.
1. Private instance attributes는 __double_leading_underscore 형식을 따른다.
1. Class, Except는 CapitalizedWord 형식을 따른다.
1. 모듈에서의 상수는 ALL_CAPS 형식을 따른다.
1. 클래스의 메소드(함수)는 첫 번째 파라미터의 이름을 self로 지정한다.
1. 클래스 메소드에서는 첫 번째 파라미터의 이름을 cls로 지정한다.


## MySql
### Transaction Isolation
- Transaction Isolation Level

    - READ UNCOMMITTED

        다른 트랜잭션이 Commit 전 상태를 볼 수 있음
        Binary Log가 자동으로 Row Based로 기록됨 (Statement설정 불가, Mixed 설정 시 자동 변환)
    
    - READ-COMMITTED

        Commit된 내역을 읽을 수 있는 상태로, 트랜잭션이 다르더라도 특정 타 트랜잭션이 Commit을 수행하면 해당 데이터를 Read할 수 있음
        Binary Log가 자동으로 Row Based로 기록됨 (Statement설정 불가, Mixed 설정 시 자동 변환)
    
    - REPEATABLE READ

        MySQL InnoDB 스토리지 엔진의 Default Isolation Level
        Select 시 현재 데이터 버전의 Snapshot을 만들고, 그 Snapshot으로부터 데이터를 조회
        동일 트랜잭션 내에서 데이터 일관성을 보장하고 데이터를 다시 읽기 위해서는 트랜잭션을 다시 시작해야 함
    
    - SERIALIZABLE

        가장 높은 Isolation Level로 트랜잭션이 완료될 때까지 SELECT 문장이 사용하는 모든 데이터에 Shared Lock이 걸림
        다른 트랜잭션에서는 해당 영역에 관한 데이터 변경 뿐만 아니라 입력도 불가

- Isolation 변경
    
    `mysql> SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;`
    
    ```$xslt
    /etc/mysql/my.cnf 에 다음 사항 추가. (영구 설정)
    [mysqld]
    transaction-isolation = READ-COMMITTED
    ```