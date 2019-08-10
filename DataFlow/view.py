from django.http import HttpResponse
# from investing_strategy.gap_investing import gap_strategy
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import io
from scipy.signal import argrelextrema
import FinanceDataReader as fdr
import datetime
#한글 폰트 사용
from matplotlib import font_manager,rc
from django.shortcuts import render
import matplotlib
from django.template import Context, Template
from django.template.loader import get_template



font_path = "C:\Windows\Fonts\malgun.ttf"
font_name = font_manager.FontProperties(fname=font_path).get_name()
matplotlib.rc('font',family=font_name)


# https://stackoverflow.com/questions/49542459/error-in-django-when-using-matplotlib-examples
class draw_upper_lower_plot:
    def __init__(self, code:str, start:str, end:str):
        self.code = code
        self.start = start
        self.end = end
        self.df = fdr.DataReader(self.code, self.start, self.end)
        self.arr_close = np.array(self.df['Close'])

    def get_stock(self):
        return fdr.DataReader(self.code, self.start, self.end)

    def _local_maxia(self, arr):
        return argrelextrema(arr, np.greater_equal, order=30, mode='clip')

    def _local_minima(self, arr):
        return argrelextrema(arr, np.less_equal, order=30, mode='clip')

    def get_local_maxia_index(self):
        return self.df['Close'].iloc[self._local_maxia(self.arr_close)].index

    def get_local_maxia_values(self):
        return self.df['Close'].iloc[self._local_maxia(self.arr_close)]

    def get_local_minima_index(self):
        return self.df['Close'].iloc[self._local_minima(self.arr_close)].index

    def get_local_minima_values(self):
        return self.df['Close'].iloc[self._local_minima(self.arr_close)]



def delta(start_index, end_index, start_value, end_value):
    time_delta = (start_index - end_index).days
    value_delta = start_value - end_value
    value = value_delta / time_delta
    return value

def fill_gap(end, func):
    values = []
    for i in range(1, 7):
        value = end + func * i
        values.append(value)
    return values


def hello(request):
    return HttpResponse("정미 바보")

# 동적 뷰
def current_time(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now {}s. </body></html>".format(now)
    return HttpResponse(html)

def letter(request):
    # t = get_template('DataFlow/letter.html')
    return render(request, 'DataFlow/letter.html',
                  {'person_name': '정미',
                   'company': '문화예술회관',
                   'shap_data': datetime.date(2015, 7, 2),
                   'ordered_warranty': False}
                  )


def index(request):
    # t = get_template('DataFlow/letter.html')
    return render(request, 'DataFlow/index.html')

def img_home(request):
    import matplotlib.pyplot as plt
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature

    fig = plt.figure(figsize=(12, 8))
    FigureCanvasAgg(fig)
    buf = io.BytesIO()
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

    ax.set_global()
    ax.stock_img()

    ax.add_feature(cfeature.LAND, color='wheat')
    ax.add_feature(cfeature.OCEAN, color='skyblue')
    ax.add_feature(cfeature.COASTLINE, linestyle='-', lw=1)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.add_feature(cfeature.LAKES, alpha=0.5, color='y')
    ax.add_feature(cfeature.RIVERS, color='skyblue', alpha=0.3)
    ax.plot(18.4241, -33.9249, 'o', transform=ccrs.Geodetic(), markersize=7, color='r', alpha=0.3)
    plt.text(18.4241, -33.9249, 'Cape Town', size=10, color='indigo', horizontalalignment='left',
             transform=ccrs.Geodetic())
    plt.savefig(buf, format='png')
    plt.close(fig)
    response = HttpResponse(buf.getvalue(), content_type='image/png')
    return response






# 대한유화
def _006650(request):
    plt.close()
    f = Figure(figsize=(30, 20))

    # Code that sets up figure goes here; in the question, that's ...
    FigureCanvasAgg(f)
    stock_df = draw_upper_lower_plot('006650', '2010-01-01', '2019-06-10')

    local_minima_index = stock_df.get_local_minima_index()
    local_minima_values = stock_df.get_local_minima_values()

    local_maxima_index = stock_df.get_local_maxia_index()
    local_maxima_values = stock_df.get_local_maxia_values()
    buf = io.BytesIO()
    plt.plot(stock_df.get_stock()['Close'])
    plt.plot(local_minima_index, local_minima_values)
    plt.plot(local_maxima_index, local_maxima_values)
    # under_predict
    # upper_predict
    predict_under_index = [local_minima_index[-1] + datetime.timedelta(days=i) for i in range(1, 7)]
    predict_upper_index = [local_maxima_index[-1] + datetime.timedelta(days=i) for i in range(1, 7)]
    predict_under_value = fill_gap(local_minima_values[-1], delta(local_minima_index[-1], local_minima_index[-2],
                                                                  local_minima_values[-1], local_minima_values[-2]))
    predict_upper_value = fill_gap(local_maxima_values[-1], delta(local_maxima_index[-1], local_maxima_index[-2],
                                                                  local_maxima_values[-1], local_maxima_values[-2]))
    plt.title('대한유화 ,매도가 : {}원, 매수가 : {}원'.format(int(predict_upper_value[-1]), int(predict_under_value[-1])))
    plt.plot(predict_under_index, predict_under_value, linestyle='--', color='b')
    plt.plot(predict_upper_index, predict_upper_value, linestyle='--', color='r')
    plt.xticks(rotation='vertical')
    plt.savefig(buf, format='png')
    plt.close(f)
    response = HttpResponse(buf.getvalue(), content_type='image/png')
    return response

# OCI

# upper, under 실제 인덱스 값으로 이동시킬 것
def _010060(request):
    plt.close()
    f = Figure(figsize=(30, 20))

    # Code that sets up figure goes here; in the question, that's ...
    FigureCanvasAgg(f)
    stock_df = draw_upper_lower_plot('010060', '2019-01-01', '2019-06-10')

    local_minima_index = stock_df.get_local_minima_index()
    local_minima_values = stock_df.get_local_minima_values()

    local_maxima_index = stock_df.get_local_maxia_index()
    local_maxima_values = stock_df.get_local_maxia_values()
    buf = io.BytesIO()
    plt.plot(stock_df.get_stock()['Close'])
    plt.plot(local_minima_index, local_minima_values)
    plt.plot(local_maxima_index, local_maxima_values)
    # under_predict
    # upper_predict
    predict_under_index = [local_minima_index[-1] + datetime.timedelta(days=i) for i in range(1, 7)]
    predict_upper_index = [local_maxima_index[-1] + datetime.timedelta(days=i) for i in range(1, 7)]
    predict_under_value = fill_gap(local_minima_values[-1], delta(local_minima_index[-1], local_minima_index[-2],
                                                                  local_minima_values[-1], local_minima_values[-2]))
    predict_upper_value = fill_gap(local_maxima_values[-1], delta(local_maxima_index[-1], local_maxima_index[-2],
                                                                  local_maxima_values[-1], local_maxima_values[-2]))
    plt.title('OCI ,매도가 : {}원, 매수가 : {}원'.format(int(predict_upper_value[-1]), int(predict_under_value[-1])))
    plt.plot(predict_under_index, predict_under_value, linestyle='--', color='b')
    plt.plot(predict_upper_index, predict_upper_value, linestyle='--', color='r')
    plt.xticks(rotation='vertical')
    plt.savefig(buf, format='png')
    plt.close(f)
    response = HttpResponse(buf.getvalue(), content_type='image/png')
    return response

# 헬릭스미스
def _084990(request):
    plt.close()
    f = Figure(figsize=(30, 20))

    # Code that sets up figure goes here; in the question, that's ...
    FigureCanvasAgg(f)
    stock_df = draw_upper_lower_plot('084990', '2019-01-01', '2019-06-10')

    local_minima_index = stock_df.get_local_minima_index()
    local_minima_values = stock_df.get_local_minima_values()

    local_maxima_index = stock_df.get_local_maxia_index()
    local_maxima_values = stock_df.get_local_maxia_values()
    buf = io.BytesIO()
    predict_under_index = [local_minima_index[-1] + datetime.timedelta(days=i) for i in range(1, 7)]
    predict_upper_index = [local_maxima_index[-1] + datetime.timedelta(days=i) for i in range(1, 7)]
    predict_under_value = fill_gap(local_minima_values[-1], delta(local_minima_index[-1], local_minima_index[-2],
                                                                  local_minima_values[-1], local_minima_values[-2]))
    predict_upper_value = fill_gap(local_maxima_values[-1], delta(local_maxima_index[-1], local_maxima_index[-2],
                                                                  local_maxima_values[-1], local_maxima_values[-2]))
    plt.title('헬릭스미스 ,매도가 : {}원, 매수가 : {}원'.format(int(predict_upper_value[-1]), int(predict_under_value[-1])))
    plt.plot(predict_under_index, predict_under_value, linestyle='--', color='b')
    plt.plot(predict_upper_index, predict_upper_value, linestyle='--', color='r')
    plt.xticks(rotation='vertical')
    plt.savefig(buf, format='png')
    plt.close(f)
    response = HttpResponse(buf.getvalue(), content_type='image/png')
    return response
