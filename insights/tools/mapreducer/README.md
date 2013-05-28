mapreducer
=======

appspand에 남겨지는 데이타를 주기적으로(1시간) 통합하여 하나의 collection으로 만들고,
(필요에 따라 여러개로 분화될 수 있음) Map/Reduce를 실행하는 모쥴.

config/config.js: db & server configuration

model/statsReport.js: map/reduce 실행후 처리결과(실행시간, 실행건수 등)를 남기는 schema. mongojs로 변경후 사용하지 않음

process/integrator.js: event.all, event.cpu의 통합 collection 생성(join)

process/map-reduce-mongoose-template.js: 통합 collection에 대한 map/reduce 실행템플릿

lib/dataProcessor.js: integrator와 map-reduce를 주기적으로 돌려주는 scheduler


