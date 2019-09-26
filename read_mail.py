import smtplib
import time
import imaplib
import email
import pandas as pd
ORG_EMAIL   = "@gmail.com"
FROM_EMAIL  = "***********"
FROM_PWD    = "*******"
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT   = 993

def read_email_from_gmail():
	subject = []
	sender = []
	date = []
	mail = imaplib.IMAP4_SSL(SMTP_SERVER)
	print(FROM_EMAIL,FROM_PWD)
	mail.login(FROM_EMAIL,FROM_PWD)
	mail.select('inbox')
	type, data = mail.search(None, 'ALL')
	mail_ids = data[0]
	id_list = mail_ids.split()   
	first_email_id = int(id_list[0])
	latest_email_id = int(id_list[-1])
	# latest_email_id = 438
	print(latest_email_id)
	for i in range(latest_email_id,first_email_id, -1):
		typ, data = mail.fetch(str(i), '(RFC822)' )
		email_content = data[0][1]
		msg = email.message_from_bytes(email_content) # this needs to be corrected in your case
		dt = msg["Date"]
		dt_list = dt.split(' ')
		print(dt_list)
		# exit()
		if len(dt_list)>5:
			day = int(dt_list[1])
		else:
			day = int(dt_list[0])
		if day>=10:
			subject.append(msg["Subject"])
			date.append(msg["Date"])
			sender.append(msg["from"])
			dfdata = {'From': sender, 'Date': date, 'Subject': subject}
			df = pd.DataFrame(dfdata)
			print(df)
			df.to_csv('email_details_3.csv')
		else:
			break

def final_csv():
	df = pd.read_csv('email_details_3.csv')
	# print(df)
	name = []
	email = []
	date = []
	subject = []
	for index, row in df.iterrows():
		details = str(row['From'])
		print((details))
		if details!='nan':
			x = details.find('<')
			na = details[0:x-1]
			em = details[x+1:-1]
			name.append(na)
			email.append(em)
		else:
			name.append('')
			email.append('')
		date.append(row['Date'])
		subject.append(row['Subject'])
	dfdata = {'Sender Email': email, 'Sender Name': name, 'Date': date, 'Subject': subject}
	dfnew = pd.DataFrame(dfdata)
	dfnew.to_csv('email_details_10.csv')

read_email_from_gmail()
final_csv()