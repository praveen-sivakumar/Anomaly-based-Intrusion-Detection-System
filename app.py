from flask import Flask,render_template,url_for,request
import pandas as pd 
import pickle
import csv
import io
import os

SUPPORTED_FILE_TYPE = ['csv', 'txt']

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/predict',methods=['POST'])
def predict():
	# df= pd.read_csv("file_1.csv")
	form_data=request.files
	f=form_data['filename']
	ext = f.filename.split('.')
	if ext[-1] not in SUPPORTED_FILE_TYPE:
		message = 'unsupppored file'
	stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None) 
	df = pd.read_csv(stream)
	ip_addresses = ['28.194.195.199','51.35.110.23','224.92.183.220','189.123.196.76','241.29.247.221','59.226.145.149',
					'157.223.74.149','65.45.66.231','109.209.151.250','206.132.101.129','6.21.156.73','231.245.174.78',
					'168.4.23.196','232.84.169.74','250.156.189.37','251.8.90.238','248.0.42.120',
					'200.195.94.180','162.22.221.194','3.189.241.122','58.152.136.186','147.33.129.125',
					'234.188.235.100','212.238.32.43','2.91.63.12','87.62.160.33','43.73.89.143',
					'70.82.146.121','253.231.1.110','234.234.240.252','22.184.138.196','246.115.56.76',
					'41.66.217.209','84.156.30.164','185.173.192.65','4.58.247.77','166.113.184.67',
					'97.112.48.88','86.131.81.156','237.98.117.178','124.160.11.211','111.228.122.116',
					'131.58.225.16','229.84.182.166','49.103.115.180','110.220.241.131','141.252.128.149',
					'239.135.48.98','2.3.133.153','215.230.20.111','249.232.38.145','232.37.49.113','74.207.218.241',
					'72.136.95.43','126.6.185.147','12.240.84.139','150.46.201.112','226.74.109.18',
					'56.59.179.51','156.107.249.218','230.96.221.108','216.190.141.78','211.103.213.41','77.131.38.69',
					'198.108.238.236','151.212.15.198','118.166.184.148','93.72.20.216','125.166.61.235',
					'18.124.252.228','56.52.221.93','5.165.229.174','113.113.112.60','177.204.227.191',
					'189.105.125.47','143.65.252.37','185.62.185.154','118.160.88.175','44.59.74.13',
					'206.143.104.146','89.157.187.217','90.171.34.14','207.20.129.101','185.73.167.144',
					'181.128.207.98','36.38.235.116','179.28.130.76','105.97.227.110','152.181.219.88',
					'164.108.230.86','215.171.185.243','208.229.38.61','249.30.54.250','82.142.85.69',
					'217.248.207.161','205.102.214.39','240.219.22.92','194.222.71.183','214.248.211.138','216.127.195.238']
	loaded_model = pickle.load(open('finalized_model.sav', 'rb'))
	if request.method == 'POST':
		my_prediction = loaded_model.predict(df)
		my_pred = my_prediction.tolist()[:100]
		data={}
		for i in range(len(ip_addresses)):
			data[ip_addresses[i]] = my_pred[i]
		return render_template('result.html',prediction = data)

if __name__ == '__main__':
	app.run(debug=True)