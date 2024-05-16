# 이터널리턴 자동 전적검색 프로젝트
## 소개
짧은 시간 안에 팀원의 전적을 보고 조합을 맞추기 위한 프로젝트

## 기능
- 화면 캡쳐 기반 글자인식
- 기본브라우저로 팀원의 dak.gg 전적 표시
- 한/영/일 지원
- fullscreen, windowded 지원

## how to
1. [Release 에서 최선버전 zip 다운로드 ](https://github.com/LEE-ChangSeok/EternalReturn_autosearch/tags)
2. Lumia_autosearch_ori.exe 실행
3. (옵션) 기본브라우저 실행 (크롬, 엣지 등)
4. Eternal Return 실행
5. 매치메이킹
6. 기본브라우저에 열린 dak.gg에서 팀원 전적 확인

## 기술
- Tesseract OCR https://github.com/tesseract-ocr/tesseract
- Python
-- PIL, urllib, webbrowser패키지 등
- dxcam https://github.com/ra1nty/DXcam

## todo
- 버그수정
- 파일사이즈 경량화
- 동작 최적화 
