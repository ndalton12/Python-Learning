# -*- coding: utf-8 -*-

BOT_NAME = 'livingsocial'

SPIDER_MODULES = ['scraper_app.spiders']

DATABASE = {
    'drivername': 'postgres',
    'host': 'localhost',
    'port': '5432',
    'username': '',
    'password': '',
    'database': 'living_social'
}

ITEM_PIPELINES = {'scraper_app.pipelines.LivingSocialPipeline':100}