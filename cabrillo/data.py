"""Constants from the Cabrillo specification.

Based on the Cabrillo specification available at
https://wwrof.org/cabrillo/cabrillo-specification-v3/
All values below should remain upper case.
"""

CATEGORY_ASSISTED = ['ASSISTED', 'NON-ASSISTED']
CATEGORY_BAND = ['ALL', '160M', '80M', '40M', '20M', '15M', '10M', '6M', '4M',
                 '2M', '222', '432', '902', '1.2G', '2.3G', '3.4G', '5.7G',
                 '10G', '24G', '47G', '75G', '123G', '134G', '241G', 'LIGHT',
                 'VHF-3-BAND', 'VHF-FM-ONLY']
CATEGORY_MODE = ['SSB', 'CW', 'RTTY', 'FM', 'MIXED']
CATEGORY_OPERATOR = ['SINGLE-OP', 'MULTI-OP', 'CHECKLOG']
CATEGORY_POWER = ['HIGH', 'LOW', 'QRP']
CATEGORY_STATION = ['FIXED', 'MOBILE', 'PORTABLE', 'ROVER', 'ROVER-LIMITED',
                    'ROVER-UNLIMITED', 'EXPEDITION', 'HQ', 'SCHOOL']
CATEGORY_TIME = ['6-HOURS', '12-HOURS', '24-HOURS']
CATEGORY_TRANSMITTER = ['ONE', 'TWO', 'LIMITED', 'UNLIMITED', 'SWL']
CATEGORY_OVERLAY = ['CLASSIC', 'ROOKIE', 'TB-WIRES', 'NOVICE-TECH', 'OVER-50']
MODES = ['CW', 'PH', 'FM', 'RY', 'DG']

KEYWORD_MAP = dict(version='START-OF-LOG', callsign='CALLSIGN',
                   contest='CONTEST', category_assisted='CATEGORY-ASSISTED',
                   category_band='CATEGORY-BAND',
                   category_mode='CATEGORY-MODE',
                   category_operator='CATEGORY-OPERATOR',
                   category_power='CATEGORY-POWER',
                   category_station='CATEGORY-STATION',
                   category_time='CATEGORY-TIME',
                   category_transmitter='CATEGORY-TRANSMITTER',
                   category_overlay='CATEGORY-OVERLAY',
                   certificate='CERTIFICATE', claimed_score='CLAIMED-SCORE',
                   club='CLUB', created_by='CREATED-BY', email='EMAIL',
                   location='LOCATION', name='NAME', address='ADDRESS',
                   address_city='ADDRESS-CITY',
                   address_state_province='ADDRESS-STATE-PROVINCE',
                   address_postalcode='ADDRESS-POSTALCODE',
                   address_country='ADDRESS-COUNTRY', operators='OPERATORS',
                   offtime='OFFTIME', soapbox='SOAPBOX', qso='QSO',
                   x_qso='X-QSO')
VALID_CATEGORIES_MAP = dict(category_assisted=CATEGORY_ASSISTED,
                            category_band=CATEGORY_BAND,
                            category_mode=CATEGORY_MODE,
                            category_operator=CATEGORY_OPERATOR,
                            category_power=CATEGORY_POWER,
                            category_station=CATEGORY_STATION,
                            category_time=CATEGORY_TIME,
                            category_transmitter=CATEGORY_TRANSMITTER,
                            category_overlay=CATEGORY_OVERLAY)
