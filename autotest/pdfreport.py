# rom reportlab.graphics.shapes import Drawing
# from reportlab.graphics.charts.barcharts import VerticalBarChart
# from urllib import urlopen
# from reportlab.graphics.shapes import *
# from reportlab.graphics.charts.lineplots import LinePlot
# from reportlab.graphics.charts.textlabels import Label
# from reportlab.graphics import renderPDF
# class pdfreport():
#     def createpdf(self,datas):
#         drawing = Drawing(400, 200)
#         #data = [(13, 5, 20),(14, 6, 21)]
#         data=datas
#         bc = VerticalBarChart()
#         bc.x = 50
#         bc.y = 50
#         bc.height = 125
#         bc.width = 300
#         bc.data = data
#         bc.strokeColor = colors.black
#         bc.valueAxis.valueMin = 0
#         bc.valueAxis.valueMax = 50
#         bc.valueAxis.valueStep = 10
#         bc.categoryAxis.labels.boxAnchor ='ne'
#         bc.categoryAxis.labels.dx = 8
#         bc.categoryAxis.labels.dy = -2
#         bc.categoryAxis.labels.angle = 30
#         bc.categoryAxis.categoryNames = ['Jan-99','Feb-99','Mar-99']
#         #bc.categoryAxis.categoryNames =ytype
#         drawing.add(bc)
#
#         drawing.add(String(250,150,"ss", fontSize=14,fillColor=colors.red))
#         #drawing.add(String(250,150,des, fontSize=14,fillColor=colors.red))
#         renderPDF.drawToFile(drawing,'report1.pdf','API')
#         #renderPDF.drawToFile(drawing,'APIReport.pdf','API')
#
# datas=[(0,20),(0,25)]
# f=pdfreport()
# f.createpdf(datas)
