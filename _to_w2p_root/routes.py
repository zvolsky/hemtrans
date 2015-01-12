#!/usr/bin/python
# -*- coding: utf-8 -*-

default_application = 'hemtrans'    # ordinarily set in base routes.py
default_controller = 'default'  # ordinarily set in app-specific routes.py
default_function = 'index'      # ordinarily set in app-specific routes.py

routes_in = (
  ('/$anything', '/hemtrans/$anything'),
  ('*./favicon.ico', '/hemtrans/static/images/favicon.ico'),
  ('*./favicon.png', '/hemtrans/static/images/favicon.png'),
  ('*./robots.txt', '/hemtrans/static/robots.txt'),
  )

routes_out = [(x, y) for (y, x) in routes_in[:-3]]
