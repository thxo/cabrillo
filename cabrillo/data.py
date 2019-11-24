"""Constants from the Cabrillo specification.

Based on the Cabrillo specification available at
https://wwrof.org/cabrillo/cabrillo-specification-v3/
All values below should remain upper case.
"""

import collections

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

# Fields that will be output in the sequence given here.
# Does not include START-OF-LOG nor QSO nor X-QSO,
# which will be treated specifically.
OUTPUT_KEYWORD_MAP = collections.OrderedDict()

OUTPUT_KEYWORD_MAP['callsign'] = 'CALLSIGN'
OUTPUT_KEYWORD_MAP['operators'] = 'OPERATORS'
OUTPUT_KEYWORD_MAP['contest'] = 'CONTEST'
OUTPUT_KEYWORD_MAP['claimed_score'] = 'CLAIMED-SCORE'
OUTPUT_KEYWORD_MAP['certificate'] = 'CERTIFICATE'
OUTPUT_KEYWORD_MAP['category_operator'] = 'CATEGORY-OPERATOR'
OUTPUT_KEYWORD_MAP['category_assisted'] = 'CATEGORY-ASSISTED'
OUTPUT_KEYWORD_MAP['category_band'] = 'CATEGORY-BAND'
OUTPUT_KEYWORD_MAP['category_power'] = 'CATEGORY-POWER'
OUTPUT_KEYWORD_MAP['category_mode'] = 'CATEGORY-MODE'
OUTPUT_KEYWORD_MAP['category_station'] = 'CATEGORY-STATION'
OUTPUT_KEYWORD_MAP['category_time'] = 'CATEGORY-TIME'
OUTPUT_KEYWORD_MAP['category_transmitter'] = 'CATEGORY-TRANSMITTER'
OUTPUT_KEYWORD_MAP['category_overlay'] = 'CATEGORY-OVERLAY'
OUTPUT_KEYWORD_MAP['offtime'] = 'OFFTIME'
OUTPUT_KEYWORD_MAP['club'] = 'CLUB'
OUTPUT_KEYWORD_MAP['name'] = 'NAME'
OUTPUT_KEYWORD_MAP['email'] = 'EMAIL'
OUTPUT_KEYWORD_MAP['location'] = 'LOCATION'
OUTPUT_KEYWORD_MAP['address'] = 'ADDRESS'
OUTPUT_KEYWORD_MAP['address_city'] = 'ADDRESS-CITY'
OUTPUT_KEYWORD_MAP['address_state_province'] = 'ADDRESS-STATE-PROVINCE'
OUTPUT_KEYWORD_MAP['address_postalcode'] = 'ADDRESS-POSTALCODE'
OUTPUT_KEYWORD_MAP['address_country'] = 'ADDRESS-COUNTRY'
OUTPUT_KEYWORD_MAP['created_by'] = 'CREATED-BY'
OUTPUT_KEYWORD_MAP['soapbox'] = 'SOAPBOX'

# Keywords we accept on input.
KEYWORD_MAP = dict(OUTPUT_KEYWORD_MAP, version='START-OF-LOG', qso='QSO', x_qso='X-QSO')

VALID_CATEGORIES_MAP = dict(category_assisted=CATEGORY_ASSISTED,
                            category_band=CATEGORY_BAND,
                            category_mode=CATEGORY_MODE,
                            category_operator=CATEGORY_OPERATOR,
                            category_power=CATEGORY_POWER,
                            category_station=CATEGORY_STATION,
                            category_time=CATEGORY_TIME,
                            category_transmitter=CATEGORY_TRANSMITTER,
                            category_overlay=CATEGORY_OVERLAY)
VALID_QSO_CATEGORIES = ['1800', '3500', '7000', '14000', '21000', '28000',
                        '50', '70', '144', '222', '432', '902', '1.2G', '2.3G',
                        '3.4G', '5.7G', '10G', '24G', '47G', '75G', '123G',
                        '134G', '241G', 'LIGHT']
FREQ_RANGES = {'1800': (1800, 2000),
               '3500': (3500, 4000),
               '7000': (7000, 7300),
               '14000': (14000, 14350),
               '21000': (21000, 21450),
               '28000': (28000, 29700)}
