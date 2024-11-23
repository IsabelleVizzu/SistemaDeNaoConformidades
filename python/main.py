import os
from flask import Flask, render_template, request, redirect, url_for
from trello import TrelloClient
from Trello import Trello
from Document import Document
from Email import Email
import time
import threading

#TOKEN = 'ATTAc8e04c1d8e0c8f9055e618534d5c95708386c0fe83060ee96498ccfcefd1f76cA452D6D0'

API_KEY = 'coloque a sua chave aqui'
API_SECRET = 'coloque a sua/seu senha/segredo da chave aqui'
TOKEN = 'coloque seu token aqui'
board_id = 'coloque o id do seu board aqui'
non_conformity_list = 'coloque o id da sua lista de não conformidades aqui'
geral_feedback_list = 'coloque o id da sua lista de feedback aqui'
higher_review_list = 'coloque o id da sua lista de atrasados aqui'
resolved_list = 'coloque o id da sua lista de resolvidos aqui'
file_path = os.path.join(os.getcwd(), 'checklist.csv')
email = "coloque seu email aqui"
password = 'coloque a senha do email aqui'


trello = Trello(API_KEY, API_SECRET, TOKEN, board_id)
email = Email(email, password)
checklist = Document(file_path)


if trello.cards == []:
    for non_conformity in checklist.non_conformities:
        trello.verify_card(non_conformity_list, higher_review_list, resolved_list, non_conformity[0], non_conformity[4],
                           non_conformity[2], non_conformity[3], non_conformity[5], non_conformity[7], non_conformity[6], email, checklist)

trello.checking_deadline()
trello.feedback_update(geral_feedback_list, checklist.get_number_of_rows(), checklist.non_conformities, checklist)
trello.organize_cards(non_conformity_list)
for non_comformity in trello.cards:
    print(non_comformity.non_conformity)

thread1 = threading.Thread(target=trello.run_deadline_checker, args=(non_conformity_list, resolved_list, higher_review_list,))
thread1.start()

trello.organize_cards(higher_review_list)
print("ola :)")

