# GoToPass1
  <p>Этот сайт написан на Python/Django для летнего лагеря.</p>
  <p>В начале смены, организатор открывает сайт, вводит ФИО ребёнка и номер комнаты в которой он живёт. Всё это отправляется на сервер 
и хранится в базе данных. Сервер же, в свою очередь, выдаёт pdf документ, который идёт на печать. В этом документе может находится памятка
для ребёнка, правила поведения или какая-либо инструкция, а так же ФИО ребёнка и QR-код с уникальным токеном, который так же хранится в
базе.</p>
  <p>В дальнейшем этот токен можно привязать к id в Telegram или в других соц. сетях и использовать как идентефикацию личности ребёнка по нику для участия в други сервисах этого лагеря.</p>