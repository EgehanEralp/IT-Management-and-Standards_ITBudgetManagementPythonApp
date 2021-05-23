#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 21:30:47 2021

@author: egehaneralp
"""

from flask import Flask, render_template, request,send_file
import pandas as pd
from pandas_profiling import ProfileReport
import numpy as np

app = Flask(__name__)

@app.route('/')
def first():
   return render_template('index.html')


@app.route('/hesapla', methods = ['GET','POST'])
def hesapla():
   if request.method == "POST":
       butceTuru = request.form.get("butceturu")
       aciklama = request.form.get("aciklama")
       miktar = request.form["miktar"]
       miktar = int(miktar)
       ayYil = request.form.get("ayyil")
       
       print(butceTuru +"\t"+ aciklama +"\t"+ str(miktar) +"\t"+ ayYil)
       
       if (ayYil == "Aylık"):
           aylıkMiktar = miktar
           yıllıkMiktar = aylıkMiktar * 12
       else:#Yıllık
           yıllıkMiktar = miktar
           aylıkMiktar = yıllıkMiktar / 12
           aylıkMiktar = "{:.2f}".format(aylıkMiktar)
       
       
       #gelir
       if (butceTuru == "Proje Bazlı Gelir" or butceTuru == "Rutin Gelir"):
           dataSetName = "gelir.pkl"
           try:
               dataSet = pd.read_pickle(dataSetName)
           except FileNotFoundError:
               data = {'Tür':[] ,'Açıklama':[] ,'YıllıkBütçe':[] ,'AylıkBütçe':[]}
               data = pd.DataFrame(data)
               data.to_pickle(dataSetName)
               dataSet = pd.read_pickle(dataSetName)
        
           newInput = {'Tür':[butceTuru], 'Açıklama':[aciklama] ,'YıllıkBütçe':[yıllıkMiktar], 'AylıkBütçe':[aylıkMiktar]}
           newInput = pd.DataFrame(newInput)
           dataSet = dataSet.append(newInput, ignore_index=True)
           #added 4
           dataSet['Tür'] = dataSet.Tür.astype(str)
           dataSet['Açıklama'] = dataSet.Açıklama.astype(str)
           dataSet["AylıkBütçe"] = pd.to_numeric(dataSet["AylıkBütçe"], downcast="float")
           dataSet["YıllıkBütçe"] = pd.to_numeric(dataSet["YıllıkBütçe"], downcast="float")
           
           dataSet.to_pickle(dataSetName)

       elif (butceTuru == "Sabit Gider" or butceTuru == "Değişken Gider"):
           dataSetName = "gider.pkl"
           try:
               dataSet = pd.read_pickle(dataSetName)
           except FileNotFoundError:
               data = {'Tür':[],'Açıklama':[] ,'YıllıkBütçe':[] ,'AylıkBütçe':[]}
               data = pd.DataFrame(data)
               data.to_pickle(dataSetName)
               dataSet = pd.read_pickle(dataSetName)
        
           newInput = {'Tür':[butceTuru],'Açıklama':[aciklama] ,'YıllıkBütçe':[yıllıkMiktar], 'AylıkBütçe':[aylıkMiktar]}
           newInput = pd.DataFrame(newInput)
           dataSet = dataSet.append(newInput, ignore_index=True)
           #added 4
           dataSet['Tür'] = dataSet.Tür.astype(str)
           dataSet['Açıklama'] = dataSet.Açıklama.astype(str)
           dataSet["AylıkBütçe"] = pd.to_numeric(dataSet["AylıkBütçe"], downcast="float")
           dataSet["YıllıkBütçe"] = pd.to_numeric(dataSet["YıllıkBütçe"], downcast="float")
           
           dataSet.to_pickle(dataSetName)

        
   return render_template('index.html', submitted = 1)


@app.route('/analiz', methods = ['GET','POST'])
def analiz():
    dataSetName = "gelir.pkl"
    try:
        dataSetGelir = pd.read_pickle(dataSetName)
        dataSetGelir["AylıkBütçe"] = pd.to_numeric(dataSetGelir["AylıkBütçe"], downcast="float")
    except FileNotFoundError:
        return render_template('index.html', analizOlumsuz = 1)
    
    dataSetName = "gider.pkl"
    try:
        dataSetGider = pd.read_pickle(dataSetName)
        dataSetGider["AylıkBütçe"] = pd.to_numeric(dataSetGider["AylıkBütçe"], downcast="float")
    except FileNotFoundError:
        return render_template('index.html', analizOlumsuz = 1)
    
    gelirList = dataSetGelir['AylıkBütçe']
    giderList = dataSetGider['AylıkBütçe']
    
    totalGelir = sum(gelirList)
    totalGider = sum(giderList)
    
    kar = totalGelir - totalGider
    
    if(kar>0):
        kar = "{:.2f}".format(kar)
        return render_template('index.html', karMiktari = kar)
    else:
        kar = kar * -1 #Zarar olarak yazacağımız için negatifliğe gerek yok
        kar = "{:.2f}".format(kar)
        return render_template('index.html', zararMiktari = kar)
    
    return render_template('index.html', submitted = 1)
    
#kullanılmıyor    
@app.route('/gelirAnaliz', methods = ['GET','POST'])
def gelirAnaliz():
    dataSetName = "gelir.pkl"
    try:
        dataSetGelir = pd.read_pickle(dataSetName)
        dataSetGelir["AylıkBütçe"] = pd.to_numeric(dataSetGelir["AylıkBütçe"], downcast="float")
        dataSetGelir["YıllıkBütçe"] = pd.to_numeric(dataSetGelir["YıllıkBütçe"], downcast="float")
    except FileNotFoundError:
        return render_template('index.html', analizOlumsuz = 1)
    
    profile = ProfileReport(dataSetGelir, title="Pandas Profiling Report")
    profile.to_file("templates/gelirReport.html")
    return render_template("gelirReport.html")

@app.route('/giderAnaliz', methods = ['GET','POST'])
def giderAnaliz():
    dataSetName = "gider.pkl"
    try:
        dataSetGider = pd.read_pickle(dataSetName)
        dataSetGider["AylıkBütçe"] = pd.to_numeric(dataSetGider["AylıkBütçe"], downcast="float")
        dataSetGider["YıllıkBütçe"] = pd.to_numeric(dataSetGider["YıllıkBütçe"], downcast="float")
    except FileNotFoundError:
        return render_template('index.html', analizOlumsuz = 1)
    
    profile = ProfileReport(dataSetGider, title="Pandas Profiling Report")
    profile.to_file("templates/giderReport.html")
    return render_template("giderReport.html")


@app.route('/downloadGelir', methods = ['GET','POST'])
def dosyaIndirGelir():
    dataSetName = "gelir.pkl"
    try:
        dataSetGelir = pd.read_pickle(dataSetName)
        dataSetGelir["AylıkBütçe"] = pd.to_numeric(dataSetGelir["AylıkBütçe"], downcast="float")
        dataSetGelir["YıllıkBütçe"] = pd.to_numeric(dataSetGelir["YıllıkBütçe"], downcast="float")
    except FileNotFoundError:
        return render_template('index.html', analizOlumsuz = 1)
    
    dataSetGelir.to_excel("gelirVerileri.xlsx") 
    return send_file("gelirVerileri.xlsx", as_attachment=True)

@app.route('/downloadGider', methods = ['GET','POST'])
def dosyaIndirGider():
    dataSetName = "gider.pkl"
    try:
        dataSetGider = pd.read_pickle(dataSetName)
        dataSetGider["AylıkBütçe"] = pd.to_numeric(dataSetGider["AylıkBütçe"], downcast="float")
        dataSetGider["YıllıkBütçe"] = pd.to_numeric(dataSetGider["YıllıkBütçe"], downcast="float")
    except FileNotFoundError:
        return render_template('index.html', analizOlumsuz = 1)
    
    dataSetGider.to_excel("giderVerileri.xlsx") 
    return send_file("giderVerileri.xlsx", as_attachment=True)


@app.route('/goDisplayGelir', methods = ['GET','POST'])
def goDisplayGelir():
    return render_template('displayAndEdit_Gelir.html')

@app.route('/goDisplayGider', methods = ['GET','POST'])
def goDisplayGider():
    return render_template('displayAndEdit_Gider.html')

@app.route('/turnBack', methods = ['GET','POST'])
def back():
    return render_template('index.html')

#GELİR Update-Delete
def html_input(c):
    return '<form action="/editSubmitGelir" method="post"><input name="{}" value="{{}}" /></form>'.format(c)

@app.route('/gelirDisplayEdit', methods = ['GET','POST'])
def gelirDisplayAndEdit():
    dataSetName = "gelir.pkl"
    try:
        dataSetGelir = pd.read_pickle(dataSetName)
        dataSetGelir["AylıkBütçe"] = pd.to_numeric(dataSetGelir["AylıkBütçe"], downcast="float")
        dataSetGelir["YıllıkBütçe"] = pd.to_numeric(dataSetGelir["YıllıkBütçe"], downcast="float")
    except FileNotFoundError:
        return render_template('displayAndEdit_Gelir.html', analizOlumsuz = 1)
    
    htmlPageWrappedForm =  '<form action="/editSubmitGelir" method="post">'+ dataSetGelir.style.apply(highlight_max).format('<input name="df" value="{}" />').render()+'<br><button type="submit" style="color:blue;">Güncelle</button></form><br><form action="/deleteGelir" method="post">Indexe göre sil:<input type="number" name="index"><button type="submit" style="color:red;">Sil</button></form><br><br><form action="/turnBack" method="post"><button type="submit" style="color:orange;">Geri Dön</button></form>'
    #htmlPageWrappedForm =  '<form action="/editSubmitGelir" method="post">'+ dataSetGelir.style.format({c: html_input(c) for c in dataSetGelir.columns}).render()+'<button type="submit" style="color:blue;">Submit</button></form>'
    
    return htmlPageWrappedForm
    #return dataSetGelir.style.format({c: html_input(c) for c in dataSetGelir.columns}).render()
    #return dataSetGelir.style.format('<form action="/editSubmitGelir" method="post"><input name="df" value="{}" /></form>').render()

@app.route('/editSubmitGelir', methods = ['GET','POST'])
def editSubmitGelir():
    dataSetName = "gelir.pkl"
    try:
        dataSetGelir = pd.read_pickle(dataSetName)
        dataSetGelir["AylıkBütçe"] = pd.to_numeric(dataSetGelir["AylıkBütçe"], downcast="float")
        dataSetGelir["YıllıkBütçe"] = pd.to_numeric(dataSetGelir["YıllıkBütçe"], downcast="float")
    except FileNotFoundError:
        return render_template('displayAndEdit_Gelir.html', analizOlumsuz = 1)
    
    shape = dataSetGelir.shape
    df = pd.DataFrame(np.asarray(request.values.getlist('df')).reshape(shape))
    df.columns = ['Tür','Açıklama','YıllıkBütçe','AylıkBütçe']
    
    df.to_pickle(dataSetName)#Güncelle
    
    #df = pd.DataFrame(request.values.lists())
    return df.style.format('<input name="df" value="{}" />').render()+'<br>Güncelleme İşlemi Başarılı<br><form action="/turnBack" method="post"><button type="submit" style="color:orange;">Geri Dön</button></form>'


@app.route('/deleteGelir', methods = ['GET','POST'])
def deleteGelir():
    if request.method == "POST":
        index = request.form.get("index")
        index = int(index)
        dataSetName = "gelir.pkl"
        dataSetGelir = pd.read_pickle(dataSetName)        
        
        indexList = dataSetGelir.index
        if index in indexList:
            dataSetGelir = dataSetGelir.drop([index], axis=0)
            dataSetGelir.to_pickle(dataSetName) 
            return dataSetGelir.style.format('<input name="df" value="{}" />').render()+'<br>Güncelleme İşlemi Başarılı<br><form action="/turnBack" method="post"><button type="submit" style="color:orange;">Geri Dön</button></form>'

        else:
            return dataSetGelir.style.format('<input name="df" value="{}" />').render()+'<br>Geçersiz Index Girdiniz. Tabloda değişiklik olmadı. <br><form action="/turnBack" method="post"><button type="submit" style="color:orange;">Geri Dön</button></form>'

#GİDER Update-Delete
@app.route('/giderDisplayEdit', methods = ['GET','POST'])
def giderDisplayEdit():
    dataSetName = "gider.pkl"
    try:
        dataSetGelir = pd.read_pickle(dataSetName)
        dataSetGelir["AylıkBütçe"] = pd.to_numeric(dataSetGelir["AylıkBütçe"], downcast="float")
        dataSetGelir["YıllıkBütçe"] = pd.to_numeric(dataSetGelir["YıllıkBütçe"], downcast="float")
    except FileNotFoundError:
        return render_template('displayAndEdit_Gider.html', analizOlumsuz = 1)
    
    htmlPageWrappedForm =  '<form action="/editSubmitGider" method="post">'+ dataSetGelir.style.apply(highlight_max).format('<input name="df" value="{}" />').render()+'<br><button type="submit" style="color:blue;">Güncelle</button></form><br><form action="/deleteGider" method="post">Indexe göre sil:<input type="number" name="index"><button type="submit" style="color:red;">Sil</button></form><br><br><form action="/turnBack" method="post"><button type="submit" style="color:orange;">Geri Dön</button></form>'
    #htmlPageWrappedForm =  '<form action="/editSubmitGelir" method="post">'+ dataSetGelir.style.format({c: html_input(c) for c in dataSetGelir.columns}).render()+'<button type="submit" style="color:blue;">Submit</button></form>'
    
    return htmlPageWrappedForm


@app.route('/editSubmitGider', methods = ['GET','POST'])
def editSubmitGider():
    dataSetName = "gider.pkl"
    try:
        dataSetGelir = pd.read_pickle(dataSetName)
        dataSetGelir["AylıkBütçe"] = pd.to_numeric(dataSetGelir["AylıkBütçe"], downcast="float")
        dataSetGelir["YıllıkBütçe"] = pd.to_numeric(dataSetGelir["YıllıkBütçe"], downcast="float")
    except FileNotFoundError:
        return render_template('displayAndEdit_Gider.html', analizOlumsuz = 1)
    
    shape = dataSetGelir.shape
    df = pd.DataFrame(np.asarray(request.values.getlist('df')).reshape(shape))
    df.columns = ['Tür','Açıklama','YıllıkBütçe','AylıkBütçe']
    
    df.to_pickle(dataSetName)#Güncelle
    
    #df = pd.DataFrame(request.values.lists())
    return df.style.format('<input name="df" value="{}" />').render()+'<br>Güncelleme İşlemi Başarılı<br><form action="/turnBack" method="post"><button type="submit" style="color:orange;">Geri Dön</button></form>'

@app.route('/deleteGider', methods = ['GET','POST'])
def deleteGider():
    if request.method == "POST":
        index = request.form.get("index")
        index = int(index)
        dataSetName = "gider.pkl"
        dataSetGelir = pd.read_pickle(dataSetName)        
        
        indexList = dataSetGelir.index
        
        if index in indexList:#değiştir -> Satır sayısına değil, maks
            dataSetGelir = dataSetGelir.drop([index], axis=0)
            dataSetGelir.to_pickle(dataSetName) 
            return dataSetGelir.style.format('<input name="df" value="{}" />').render()+'<br>Güncelleme İşlemi Başarılı<br><form action="/turnBack" method="post"><button type="submit" style="color:orange;">Geri Dön</button></form>'
        else:
            return dataSetGelir.style.format('<input name="df" value="{}" />').render()+'<br>Geçersiz Index Girdiniz. Tabloda değişiklik olmadı. <br><form action="/turnBack" method="post"><button type="submit" style="color:orange;">Geri Dön</button></form>'

def highlight_max(s):
    is_max = s == s.max()
    return ['background-color: yellow' if v else '' for v in is_max]

if __name__ == '__main__':
   app.run()
