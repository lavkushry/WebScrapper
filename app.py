from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import logging
logging.basicConfig(filename='scrapper.log',level=logging.INFO)

app=Flask(__name__)

@app.route("/", methods = ['GET'])
def homepage():
    return render_template("index.html")

@app.route("/review",methods=['POST','GET'])
def index():
    if request.method=='POST':
        try:
            searchString=request.form['content'].replace(" ","")
            flipcart_url="https://www.flipkart.com/search?q="+searchString
            uClient=uReq(flipcart_url)
            flipcart_page=uClient.read()
            uClient.close()
            flipcart_html=bs(flipcart_page,"html.parser")
            bigBoxes=flipcart_html.findAll('div',{"class":'cPHDOP col-12-12'})
            del bigBoxes[0:3]
            box=bigBoxes[0]
            product_link="https://www.flipkart.com" + box.div.div.div.a['href']
            print(product_link)

            product_req = urlopen(product_link)
            product_page=product_req.read()
            product_page.encoding='utf-8'
            product_html=bs(product_page,'html.parser')
            commentboxes=product_html.find_all("div",{"class":"RcXBOT"})
            filename = searchString + ".csv"
            fw = open(filename, "w")
            headers = "Product, Customer Name, Rating, Heading, Comment \n"
            fw.write(headers)
            reviews = []
            for commentbox in commentboxes:
                try:
                    #name.encode(encoding='utf-8')
                    name = commentbox.div.div.find_all('p', {'class': '_2NsDsF AwS1CA'})[0].text

                except:
                    logging.info("name")

                try:
                    #rating.encode(encoding='utf-8')
                    rating = commentbox.div.div.div.div.text


                except:
                    rating = 'No Rating'
                    logging.info("rating")

                try:
                    #commentHead.encode(encoding='utf-8')
                    commentHead = commentbox.div.div.div.p.text

                except:
                    commentHead = 'No Comment Heading'
                    logging.info(commentHead)
                try:
                    comtag = commentbox.div.div.find_all('div', {'class': ''})
                    #custComment.encode(encoding='utf-8')
                    custComment = comtag[0].div.text

                except Exception as e:
                    logging.info(e)

                mydict = {"Product": searchString, "Name": name, "Rating": rating, "CommentHead": commentHead,
                          "Comment": custComment}
                reviews.append(mydict)
                logging.info("log my final result {}".format(reviews))

            client=pymongo.MongoClient("mongodb+srv://pwskills:Pwskills@cluster0.xvcbxwp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
            db =client['scrapper_eng_pwskills']
            coll_pw_eng = db['scraper_pwskills_eng']
            coll_pw_eng.insert_many(reviews)
            return render_template('result.html', reviews=reviews[0:(len(reviews)-1)])

        except Exception as e:
            logging.info(e)
            return 'something is wrong'
            # return render_template('results.html')
    else:
        return render_template('index.html')





if __name__=="__main__":
    app.run(host="0.0.0.0",port=8081)