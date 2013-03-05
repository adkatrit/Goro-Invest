#todo:  get list of all symbols from ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt
#todo:  and ftp.nasdaqtrader.com/SymbolDirectory/otherlisted.txt
#todo: pick a stock that zigs when the other one zags
#CAPM removing market risk by selling spy short
import urllib2,math,operator,pickle
from numpy import mean,std,array
from collections import defaultdict
from time import sleep

filename = 'nasdaqlisted.txt'
url = 'http://ichart.finance.yahoo.com/table.csv?a=00&b=1&c=2011&d=11&e=31&f=2011&g=d&ignore=.csv&s='
url_YTD = 'http://ichart.finance.yahoo.com/table.csv?a=10&b=8&c=2011&d=10&e=8&f=2012&g=d&ignore=.csv&s='


url=url_YTD  #set the yahoo finance date range to YTD from the default of jan 1 2011 -> dec 31 2012
prefix='YTD' #prefix for the cache file name


sharpe_data = {}
range_data = {}
def is_number(s):
    try:
        float(s) # for int, long and float
    except ValueError:
        try:
            complex(s) # for complex
        except ValueError:
            return False

    return True
def sharpe(plist): # takes a list of daily return percentages and returns the sharpe ratio
#250 is the number of trading days in one year
    plist = array(plist)
    return math.sqrt(250)*mean(plist)/std(plist)


stock_data = pickle.load( open( prefix+"sharpe.p", "rb" ) )
range_data = pickle.load( open( prefix+"range.p", "rb" ) )
stock_data.reverse()
result={}
ds={}
for i in stock_data:
    ds[i[0]] = i[1]
for i in range_data:
    result[i[0]] = ds[i[0]]*math.pow(i[1],5)

end = sorted(result.iteritems(),key=operator.itemgetter(1), reverse=True)

print len(end)


for k,v in end[:10]:
    print k,v
exit(1)


##############  above needs the below to run at least once.
if True:
    it=0
    for stock in tuple(open(filename, 'r')):
        it=it+1
        try:
            response = urllib2.urlopen(url+stock)
        except:
            continue
        html = response.read()
        close_prices = []
        line_list = html.split('\n')
        year_open=0
        year_close=0
        if len(line_list) > 249:
            for idx,line in enumerate(line_list):
                if(idx>0):
                    prev = line_list[idx-1].split(',')
                    curr = line_list[idx].split(',')
                    if(idx==1):
                        year_open=float(curr[6])
                    if(idx==250):
                        year_close=float(curr[6])

                    if(len(prev)> 5 and len(curr) > 5):
                        if(idx==0 or curr[6]=='Adj Close' or prev[6]=='Adj Close'):
                            close_prices.append(0)
                        else:
                            close_prices.append((float(prev[6])/float(curr[6]))-1)
        range_data[stock]  = math.fabs(year_open-year_close)
        sharpe_data[stock] = sharpe(close_prices)
        print it
        # if(it>10):
            # print sharpe_data
            # print
            # print range_data
            # exit(1)
    sharpe_ordered = sorted(sharpe_data.iteritems(), key=operator.itemgetter(1))
    pickle.dump(sharpe_ordered, open(prefix+"sharpe.p","wb"))

    range_ordered = sorted(range_data.iteritems(), key=operator.itemgetter(1))
    pickle.dump(range_ordered, open(prefix+"range.p","wb"))