import json
from bs4 import BeautifulSoup
import html
import requests
import pandas as pd

print("###### Informação de Filmes ######")
print("\n")
name = input("Entre com Genero/Filme: ex.: terror/a vila \n")

def get_html(url):

    link = requests.get(url).content

    soup = BeautifulSoup(link, 'html.parser')

    try:

        html_parse = soup.find("textarea", class_="paste_code")
        inside_textarea = html_parse.next_element

        soup_table = BeautifulSoup(inside_textarea, 'html.parser')
        table = soup_table.find( class_="highlight")

        return table

    except:

        print("Incorreta a leitura do HTML")

def get_html_link(url):

    link = requests.get(url).content

    soup = BeautifulSoup(link, 'html.parser')

    html_parse = soup.find("textarea", class_="paste_code")
    inside_textarea = html_parse.next_element

    soup_table = BeautifulSoup(inside_textarea, 'html.parser')
    table = soup_table.find_all( 'dd' )
    PAGE_LINK = []

    for tag in table:
        PAGE_LINK.append(tag.string)

    PAGE_LINK.append(url) 
    return (PAGE_LINK)
    

def get_movie_info(listing_url, links_url, movie_id):

 
        split_movie_id = movie_id.split("/")

        genre = split_movie_id[0]
        name = split_movie_id[1]
        
        table = get_html(listing_url)
        link = get_html(links_url)

        df_full_filmes = pd.read_html( str(table))[0]
        df_full_filmes_link = pd.read_html( str(link))[0]

        df_filter_movie = df_full_filmes.loc[(df_full_filmes['nome'] == name) & 
            (df_full_filmes['genero'] == genre) ]

        diretor_filme = df_filter_movie['diretor'].unique()[0]
        genero_filme = df_filter_movie['genero'].unique()[0]
         
        df_links = df_full_filmes_link.loc[(df_full_filmes_link['nome'] == name) ]

        df_li = df_links.get(key='link')

        PAGE_LINK = []
         

        for number_page_link in df_li:
            PAGE_LINK.append(get_html_link(number_page_link))
         
        for number_movie in PAGE_LINK:
            if name == number_movie[0] and diretor_filme == number_movie[2]:
                response_movie = (number_movie)

        response = {
            "url": response_movie[3],
            "titulo": response_movie[0],
            "genero": genero_filme,
            "diretor": response_movie[2],
            "duracao": response_movie[1]
        }

        return print( json.dumps(response,indent=4) )
 
 
get_movie_info(
    "https://pastebin.com/PcVfQ1ff",
    "https://pastebin.com/Tdp532rr",
    name)

 
  
 