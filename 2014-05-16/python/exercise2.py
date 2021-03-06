from exercise1 import *

"""
FUNCTIONS
"""

# Unifies models of the list, giving a single model
# author: Stefano Russo
def larStruct(model_list):
	finalV=[]
	finalCV=[]
	count=0
	for m in model_list:
		finalV=finalV+m[0]
		tempCV = AA(AA(lambda x: x+count))(m[1])
		finalCV=finalCV+tempCV
		count = count + len(m[0])
	return finalV,finalCV

# Translates points of a model, adding 3rd dimension if necessary
# author: Stefano Russo
def translateModel(model,tvect):
	V,CV = model
	# add 3rd dimension to points if necessary
	if len(V[0])==2 and len(tvect)==3:
		V = AA ( lambda x: x+[0.0] ) (V)
	# add 3rd dimension to tvect if necessary
	if len(V[0])==3 and len(tvect)==2:
		tvect = tvect+[0]
	V = translatePoints(V,tvect)
	return V,CV

# Rotate Model in 3D
def rotateModel(model, angles):
	points,cells = model
    # euler angles ax, ay and az are about axes z, y, x respectively
	ax,ay,az = angles
    # axis z
	points1 = [[x*COS(ax)-y*SIN(ax), x*SIN(ax)+y*COS(ax), z] for x,y,z in points]
    # axis y
	points2 = [[x*COS(ay)+z*SIN(ay), y, -x*SIN(ay)+z*COS(ay)] for x,y,z in points1]
    # axis x
	points3 = [[x, y*COS(az)-z*SIN(az), y*SIN(az)+z*COS(az)] for x,y,z in points2]
	return points3,cells

# Multiplies a lar model, giving new lar model composed by all sub-models
# author: Stefano Russo
def multiply(n,tvect,model):
	oldV,oldCV=model
	# transform points from integer to float
	oldV = AA(AA (lambda x: float(x))) (oldV)
	# add 3rd dimension to points if necessary
	if len(oldV[0])==2 and len(tvect)==3:
		oldV = AA ( lambda x: x+[0.0] ) (oldV)
	# add 3rd dimension to tvect if necessary
	if len(oldV[0])==3 and len(tvect)==2:
		tvect = tvect+[0]
	newV = oldV
	newCV = oldCV
	# each iteration multiplies the model
	for i in range(1,n):
		# translate points of "tvect*i"
		newV = newV + translatePoints(oldV, AA(lambda x: x*i)(tvect))
		# create new cells, related to above points
		newCV = newCV + AA(AA(lambda x: x+(len(oldV)*i)))(oldCV)
	return newV,newCV

# Creates a bezier curve
def bezCurve(controlPoints,dom=larDomain([5])):
	mapping = larBezierCurve(controlPoints)
	return MKPOLS(larMap(mapping)(dom))



""" MAIN BUILDING """

building = assemblyDiagramInit([1,2,6])([[44],[19,4.2],[0.1,3,3,3,3,0.5]])
# drawNumDiagram(building,GREEN,3)


""" BALCONY """

balcony = assemblyDiagramInit([3,2,3])([[0.2,36.8,7],[4,0.2],[0.3,1.5,1.5]])
balcony_p2 = assemblyDiagramInit([1,2,2])([[44],[0.1,0.1],[3.2,0.1]])
balcony = diagram2cell(balcony_p2,balcony,10)
building = insertDiagramIntoCells(balcony,[11,12,13,14,15,16,17,7,8,10,2],building,[8,9,10])
base = assemblyDiagramInit([2,2,1])([[0.2,43.8],[4,0.2],[3.3]])
building = insertDiagramIntoCells(base,[0,2,3],building,[7])
# drawNumDiagram(building,GREEN,3)


""" APARTMENTS """

plan = assemblyDiagramInit([2,1,1])([[22,22],[19],[3]])
plan = diagram2cell(larApply(s(-1,1,1))(apartment),plan,1)
plan = diagram2cell(apartment,plan,0)
# drawNumDiagram(plan,GREEN,3)

building = diagram2cell(plan,building,4)
building = diagram2cell(plan,building,3)
building = diagram2cell(plan,building,2)
building = diagram2cell(plan,building,1)
# drawNumDiagram(building,GREEN,3)


""" ROOF """

roof = assemblyDiagramInit([3,2,2])([[0.3,43.4,0.3],[0.3,18.7],[0.3,0.2]])
building = insertDiagramIntoCells(roof,[7],building,[1])
roof_p2 = assemblyDiagramInit([3,2,2])([[0.3,43.4,0.3],[4,0.3],[0.3,0.2]])
building = insertDiagramIntoCells(roof_p2,[5],building,[2])
# drawNumDiagram(building,GREEN,0.5)


""" STAIRS """

# single step
p1_V = [[0.16,0.10],[0.21,0.10],[0,0.3],[0.16,0.3],[0.21,0.3],[0.5,0.3],[0,0.4],[0.5,0.4]]
p1_FV = [[0,1,3,4,0],[2,3,4,5,7,6,2]]
p2_V = [[0,-0.05],[0,0],[0.5,0.3],[0.5,0.25]]
p2_FV = [[0,1,2,3]]
step = larStruct([(p1_V,p1_FV),(p2_V,p2_FV)])

# step 3D
mod_1d = [[0.0],[-2.0]],[[0,1]]
step_3D = rotateModel(larModelProduct([step,mod_1d]),(0,0,PI/2))

# embedding stairs in building
ramp1 = multiply(5,[0.5,0,0.3],step_3D)
ramp2 = translateModel(rotateModel(ramp1,(PI,0,0)),[2.5,0,1.5])
flat = larIntervals([1,1,1])([1.5,4,0.05])
flat = translateModel(flat,[2.5,-2,1.45])

# three ramps
full_ramp = translateModel(larStruct([ramp1,ramp2,flat]),[37,21,0.05])
ramps = multiply(3,[0,0,3.05],full_ramp)


""" FULL BUILDING """

# coloring building's doors
#
# NOTA: semplice colorazione applicata manualmente alle singole celle delle porte 
# frontali. Non sono state utilizate catene, poiche' sarebbe stata necessaria una 
# parziale riscrittura del codice.

color_building = MKPOLS(building)
color_building[487] = COLOR(Color4f([(0.4),(0.28),(0)]))(color_building[487])
color_building[258] = COLOR(Color4f([(0.4),(0.28),(0)]))(color_building[258])
color_building[945] = COLOR(Color4f([(0.4),(0.28),(0)]))(color_building[945])
color_building[716] = COLOR(Color4f([(0.4),(0.28),(0)]))(color_building[716])
color_building[1403] = COLOR(Color4f([(0.4),(0.28),(0)]))(color_building[1403])
color_building[1174] = COLOR(Color4f([(0.4),(0.28),(0)]))(color_building[1174])
color_building[1632] = COLOR(Color4f([(0.4),(0.28),(0)]))(color_building[1632])
color_building[1861] = COLOR(Color4f([(0.4),(0.28),(0)]))(color_building[1861])

# complete building
full_building = COLOR(P_SBROWN)(STRUCT( color_building + MKPOLS(ramps) ))

# VIEW(full_building)


""" DECORATIONS """

dom2D = R([2,3])(PI)(EMBED(1)(PROD([GRID([.05]*20),GRID([2*PI/30]*30)])))

# GRASS
grass = COLOR(P_GREEN)(CUBOID([60,60,0.5]))

# STAIRS GLASS
glass1 = bezCurve([[5.5, 2.2], [5.73, 1.84], [5.45, 1.33], [5.71, 1.25]],larDomain([8]))
glass2 = bezCurve([[5.71, 1.25], [6.0, 1.17], [6.1, 1.28], [6.54, 1.25]],larDomain([8]))
glass = OFFSET([0.01,0.01])(STRUCT(glass1+glass2))
glass = MATERIAL(glass_material)(PROD([R([1,2])(PI)(glass),Q(2.6)]))

# FOUNTAIN
fountain_cp = [[3.42,0,0.02], [2.61,0,1.56], [5.66,0,2.07], [5.66,0,3.89]]
fountain_profile = BEZIER(S1)(fountain_cp)
fountain_map = ROTATIONALSURFACE(fountain_profile)
fountain = COLOR(P_DGRAY)(MAP(fountain_map)(dom2D))
fountain_base = COLOR(P_DGRAY)(T(3)(0.01)(CIRCLE(3.4)((20,1))))
fountain_water =  MATERIAL(water_material)(T(3)(3.7)(PROD([CIRCLE(5.6)((20,1)),Q(0.1)])))
rod = COLOR(P_DGRAY)(CYLINDER([0.1,8])(10))
z_cp = [[1.2,0,1.48], [1.17,0,2.62], [1.54,0,4.13], [2.03,0,2.87]]
z_profile = BEZIER(S1)(z_cp)
z = OFFSET([0.05,0.05,0.05])(MAP(z_profile)(dom2D))
z = T([1,2,3])([-5.1,-0.1,0.8]) ( S([1,2,3])([2.5,2.5,2.5]) (MATERIAL(water_material)(z)) )
z2 = STRUCT(NN(2)([z, R([1,2])(PI)]))
fountain_and_water = S([1,2,3])([0.3,0.3,0.3])(STRUCT([fountain,fountain_base,fountain_water,rod,z2]))

# GARDEN POT
pot_cp = [[1.14,0,0.0], [2.1,0,1.38], [0.46,0,1.53], [1.13,0,2.27]]
pot_profile = BEZIER(S1)(pot_cp)
pot_map = ROTATIONALSURFACE(pot_profile)
pot_side = COLOR(P_DGRAY)(MAP(pot_map)(dom2D))
pot_base = COLOR(P_DGRAY)(T(3)(0.01)(CIRCLE(1.1)((20,1))))
pot = S([1,2,3])([0.3,0.3,0.3])(STRUCT([pot_side,pot_base]))

# TUX!
#
# Following instructions are automatically built with a script made by me.
# The script coverts an SVG file with CUBIC-BEZIER / POLYLINE path into commands needed
# to draw the figure.

tux1 = bezCurve([[8.16, 8.94], [8.05, 8.94], [7.93, 8.94], [7.81, 8.93]])
tux2 = bezCurve([[7.81, 8.93], [4.78, 8.68], [5.59, 5.48], [5.54, 4.41]])
tux3 = bezCurve([[5.54, 4.41], [5.48, 3.63], [5.33, 3.01], [4.79, 2.24]])
tux4 = bezCurve([[4.79, 2.24], [4.15, 1.49], [3.26, 0.27], [2.84, -1.0]])
tux5 = bezCurve([[2.84, -1.0], [2.64, -1.6], [2.55, -2.21], [2.63, -2.78]])
tux6 = bezCurve([[2.63, -2.78], [2.61, -2.81], [2.58, -2.83], [2.56, -2.86]])
tux7 = bezCurve([[2.56, -2.86], [2.37, -3.06], [2.23, -3.3], [2.08, -3.46]])
tux8 = bezCurve([[2.08, -3.46], [1.94, -3.6], [1.73, -3.66], [1.51, -3.74]])
tux9 = bezCurve([[1.51, -3.74], [1.29, -3.82], [1.04, -3.94], [0.89, -4.22]])
tux10 = bezCurve([[0.89, -4.22], [0.89, -4.22], [0.89, -4.22], [0.89, -4.22]])
tux11 = bezCurve([[0.89, -4.22], [0.89, -4.22], [0.89, -4.22], [0.89, -4.23]])
tux12 = [POLYLINE([[0.89, -4.23], [0.89, -4.23]])]
tux13 = bezCurve([[0.89, -4.23], [0.75, -4.48], [0.8, -4.77], [0.84, -5.04]])
tux14 = bezCurve([[0.84, -5.04], [0.88, -5.31], [0.92, -5.56], [0.86, -5.73]])
tux15 = bezCurve([[0.86, -5.73], [0.69, -6.22], [0.66, -6.55], [0.79, -6.8]])
tux16 = bezCurve([[0.79, -6.8], [0.91, -7.04], [1.17, -7.15], [1.46, -7.21]])
tux17 = bezCurve([[1.46, -7.21], [2.04, -7.33], [2.83, -7.3], [3.45, -7.63]])
tux18 = [POLYLINE([[3.45, -7.63], [3.5, -7.53]])]
tux19 = [POLYLINE([[3.5, -7.53], [3.45, -7.63]])]
tux20 = bezCurve([[3.45, -7.63], [4.11, -7.98], [4.79, -8.1], [5.32, -7.98]])
tux21 = bezCurve([[5.32, -7.98], [5.71, -7.89], [6.03, -7.66], [6.19, -7.3]])
tux22 = bezCurve([[6.19, -7.3], [6.61, -7.3], [7.07, -7.12], [7.81, -7.08]])
tux23 = bezCurve([[7.81, -7.08], [8.31, -7.04], [8.94, -7.26], [9.66, -7.22]])
tux24 = bezCurve([[9.66, -7.22], [9.68, -7.29], [9.7, -7.37], [9.74, -7.44]])
tux25 = bezCurve([[9.74, -7.44], [9.74, -7.44], [9.74, -7.44], [9.74, -7.44]])
tux26 = bezCurve([[9.74, -7.44], [10.02, -8.0], [10.54, -8.26], [11.09, -8.21]])
tux27 = bezCurve([[11.09, -8.21], [11.65, -8.17], [12.24, -7.84], [12.71, -7.28]])
tux28 = [POLYLINE([[12.71, -7.28], [12.62, -7.2]])]
tux29 = [POLYLINE([[12.62, -7.2], [12.71, -7.27]])]
tux30 = bezCurve([[12.71, -7.27], [13.16, -6.72], [13.92, -6.5], [14.41, -6.2]])
tux31 = bezCurve([[14.41, -6.2], [14.66, -6.05], [14.87, -5.86], [14.88, -5.58]])
tux32 = bezCurve([[14.88, -5.58], [14.9, -5.31], [14.74, -5.0], [14.37, -4.59]])
tux33 = [POLYLINE([[14.37, -4.59], [14.37, -4.59]])]
tux34 = bezCurve([[14.37, -4.59], [14.37, -4.59], [14.37, -4.59], [14.37, -4.59]])
tux35 = bezCurve([[14.37, -4.59], [14.25, -4.46], [14.19, -4.2], [14.13, -3.93]])
tux36 = bezCurve([[14.13, -3.93], [14.06, -3.66], [13.99, -3.37], [13.77, -3.18]])
tux37 = [POLYLINE([[13.77, -3.18], [13.77, -3.18]])]
tux38 = bezCurve([[13.77, -3.18], [13.77, -3.18], [13.77, -3.18], [13.77, -3.18]])
tux39 = [POLYLINE([[13.77, -3.18], [13.77, -3.18]])]
tux40 = bezCurve([[13.77, -3.18], [13.68, -3.1], [13.59, -3.05], [13.5, -3.02]])
tux41 = bezCurve([[13.5, -3.02], [13.81, -2.1], [13.69, -1.19], [13.37, -0.37]])
tux42 = bezCurve([[13.37, -0.37], [12.99, 0.64], [12.32, 1.53], [11.81, 2.13]])
tux43 = bezCurve([[11.81, 2.13], [11.24, 2.85], [10.69, 3.53], [10.7, 4.54]])
tux44 = bezCurve([[10.7, 4.54], [10.71, 6.08], [10.87, 8.94], [8.16, 8.94]])
tux45 = [POLYLINE([[8.16, 8.94], [8.16, 8.94]])]
tux46 = bezCurve([[8.52, 6.57], [8.68, 6.57], [8.81, 6.52], [8.94, 6.42]])
tux47 = bezCurve([[8.94, 6.42], [9.08, 6.32], [9.18, 6.2], [9.26, 6.02]])
tux48 = bezCurve([[9.26, 6.02], [9.34, 5.85], [9.37, 5.69], [9.38, 5.49]])
tux49 = bezCurve([[9.38, 5.49], [9.38, 5.49], [9.38, 5.48], [9.38, 5.48]])
tux50 = bezCurve([[9.38, 5.48], [9.38, 5.28], [9.35, 5.1], [9.27, 4.93]])
tux51 = bezCurve([[9.27, 4.93], [9.23, 4.83], [9.18, 4.74], [9.12, 4.67]])
tux52 = bezCurve([[9.12, 4.67], [9.1, 4.68], [9.07, 4.69], [9.05, 4.7]])
tux53 = [POLYLINE([[9.05, 4.7], [9.05, 4.7]])]
tux54 = bezCurve([[9.05, 4.7], [8.9, 4.77], [8.78, 4.81], [8.69, 4.84]])
tux55 = bezCurve([[8.69, 4.84], [8.72, 4.88], [8.75, 4.93], [8.78, 5.0]])
tux56 = bezCurve([[8.78, 5.0], [8.82, 5.09], [8.83, 5.18], [8.84, 5.29]])
tux57 = bezCurve([[8.84, 5.29], [8.84, 5.3], [8.84, 5.3], [8.84, 5.31]])
tux58 = bezCurve([[8.84, 5.31], [8.84, 5.41], [8.83, 5.5], [8.8, 5.6]])
tux59 = bezCurve([[8.8, 5.6], [8.77, 5.7], [8.72, 5.77], [8.66, 5.82]])
tux60 = bezCurve([[8.66, 5.82], [8.6, 5.88], [8.54, 5.91], [8.47, 5.91]])
tux61 = bezCurve([[8.47, 5.91], [8.47, 5.91], [8.47, 5.91], [8.46, 5.91]])
tux62 = bezCurve([[8.46, 5.91], [8.4, 5.91], [8.34, 5.89], [8.28, 5.84]])
tux63 = bezCurve([[8.28, 5.84], [8.21, 5.78], [8.17, 5.72], [8.13, 5.62]])
tux64 = bezCurve([[8.13, 5.62], [8.09, 5.53], [8.07, 5.43], [8.07, 5.32]])
tux65 = bezCurve([[8.07, 5.32], [8.07, 5.32], [8.07, 5.31], [8.07, 5.31]])
tux66 = bezCurve([[8.07, 5.31], [8.06, 5.25], [8.07, 5.19], [8.08, 5.14]])
tux67 = bezCurve([[8.08, 5.14], [7.94, 5.2], [7.81, 5.25], [7.69, 5.28]])
tux68 = bezCurve([[7.69, 5.28], [7.68, 5.33], [7.68, 5.39], [7.68, 5.44]])
tux69 = [POLYLINE([[7.68, 5.44], [7.68, 5.46]])]
tux70 = bezCurve([[7.68, 5.46], [7.68, 5.66], [7.71, 5.84], [7.79, 6.01]])
tux71 = bezCurve([[7.79, 6.01], [7.86, 6.19], [7.96, 6.31], [8.09, 6.42]])
tux72 = bezCurve([[8.09, 6.42], [8.23, 6.52], [8.36, 6.57], [8.52, 6.57]])
tux73 = bezCurve([[8.52, 6.57], [8.52, 6.57], [8.52, 6.57], [8.52, 6.57]])
tux74 = [POLYLINE([[8.52, 6.57], [8.52, 6.57]])]
tux75 = bezCurve([[6.42, 6.4], [6.52, 6.4], [6.61, 6.37], [6.71, 6.29]])
tux76 = bezCurve([[6.71, 6.29], [6.81, 6.21], [6.89, 6.1], [6.95, 5.96]])
tux77 = bezCurve([[6.95, 5.96], [7.01, 5.81], [7.05, 5.66], [7.06, 5.49]])
tux78 = [POLYLINE([[7.06, 5.49], [7.06, 5.49]])]
tux79 = bezCurve([[7.06, 5.49], [7.06, 5.41], [7.06, 5.34], [7.06, 5.28]])
tux80 = bezCurve([[7.06, 5.28], [7.04, 5.27], [7.02, 5.27], [7.0, 5.26]])
tux81 = bezCurve([[7.0, 5.26], [6.89, 5.22], [6.79, 5.17], [6.71, 5.11]])
tux82 = bezCurve([[6.71, 5.11], [6.71, 5.17], [6.72, 5.23], [6.71, 5.3]])
tux83 = bezCurve([[6.71, 5.3], [6.71, 5.3], [6.71, 5.3], [6.71, 5.31]])
tux84 = bezCurve([[6.71, 5.31], [6.7, 5.4], [6.68, 5.47], [6.65, 5.54]])
tux85 = bezCurve([[6.65, 5.54], [6.62, 5.62], [6.58, 5.68], [6.53, 5.72]])
tux86 = bezCurve([[6.53, 5.72], [6.49, 5.76], [6.45, 5.77], [6.4, 5.77]])
tux87 = bezCurve([[6.4, 5.77], [6.4, 5.77], [6.39, 5.77], [6.39, 5.77]])
tux88 = bezCurve([[6.39, 5.77], [6.34, 5.77], [6.29, 5.74], [6.25, 5.7]])
tux89 = bezCurve([[6.25, 5.7], [6.21, 5.65], [6.19, 5.59], [6.17, 5.5]])
tux90 = bezCurve([[6.17, 5.5], [6.15, 5.42], [6.14, 5.34], [6.15, 5.25]])
tux91 = bezCurve([[6.15, 5.25], [6.15, 5.25], [6.15, 5.25], [6.15, 5.24]])
tux92 = bezCurve([[6.15, 5.24], [6.16, 5.15], [6.18, 5.08], [6.21, 5.01]])
tux93 = bezCurve([[6.21, 5.01], [6.24, 4.93], [6.28, 4.87], [6.33, 4.83]])
tux94 = bezCurve([[6.33, 4.83], [6.34, 4.82], [6.34, 4.82], [6.35, 4.81]])
tux95 = bezCurve([[6.35, 4.81], [6.3, 4.78], [6.28, 4.76], [6.24, 4.73]])
tux96 = bezCurve([[6.24, 4.73], [6.21, 4.71], [6.18, 4.68], [6.14, 4.66]])
tux97 = bezCurve([[6.14, 4.66], [6.06, 4.73], [6.0, 4.83], [5.94, 4.95]])
tux98 = bezCurve([[5.94, 4.95], [5.88, 5.1], [5.84, 5.24], [5.83, 5.42]])
tux99 = [POLYLINE([[5.83, 5.42], [5.83, 5.42]])]
tux100 = bezCurve([[5.83, 5.42], [5.82, 5.59], [5.84, 5.74], [5.89, 5.9]])
tux101 = bezCurve([[5.89, 5.9], [5.94, 6.05], [6.0, 6.16], [6.09, 6.26]])
tux102 = bezCurve([[6.09, 6.26], [6.18, 6.35], [6.28, 6.39], [6.39, 6.4]])
tux103 = bezCurve([[6.39, 6.4], [6.4, 6.4], [6.41, 6.4], [6.42, 6.4]])
tux104 = [POLYLINE([[6.42, 6.4], [6.42, 6.4]])]
tux105 = bezCurve([[7.37, 5.19], [7.61, 5.19], [7.9, 5.12], [8.24, 4.9]])
tux106 = bezCurve([[8.24, 4.9], [8.45, 4.76], [8.62, 4.75], [9.0, 4.58]])
tux107 = [POLYLINE([[9.0, 4.58], [9.0, 4.58]])]
tux108 = [POLYLINE([[9.0, 4.58], [9.0, 4.58]])]
tux109 = bezCurve([[9.0, 4.58], [9.18, 4.51], [9.29, 4.41], [9.34, 4.31]])
tux110 = bezCurve([[9.34, 4.31], [9.39, 4.2], [9.4, 4.09], [9.35, 3.98]])
tux111 = bezCurve([[9.35, 3.98], [9.26, 3.74], [8.98, 3.49], [8.59, 3.37]])
tux112 = [POLYLINE([[8.59, 3.37], [8.59, 3.37]])]
tux113 = [POLYLINE([[8.59, 3.37], [8.59, 3.37]])]
tux114 = bezCurve([[8.59, 3.37], [8.4, 3.31], [8.23, 3.17], [8.03, 3.06]])
tux115 = bezCurve([[8.03, 3.06], [7.84, 2.95], [7.61, 2.85], [7.31, 2.87]])
tux116 = bezCurve([[7.31, 2.87], [7.31, 2.87], [7.31, 2.87], [7.31, 2.87]])
tux117 = bezCurve([[7.31, 2.87], [7.05, 2.89], [6.9, 2.97], [6.76, 3.09]])
tux118 = bezCurve([[6.76, 3.09], [6.62, 3.2], [6.5, 3.34], [6.32, 3.44]])
tux119 = [POLYLINE([[6.32, 3.44], [6.32, 3.44]])]
tux120 = [POLYLINE([[6.32, 3.44], [6.32, 3.44]])]
tux121 = bezCurve([[6.32, 3.44], [6.03, 3.61], [5.87, 3.79], [5.83, 3.96]])
tux122 = bezCurve([[5.83, 3.96], [5.78, 4.12], [5.82, 4.26], [5.97, 4.36]])
tux123 = bezCurve([[5.97, 4.36], [6.13, 4.48], [6.24, 4.57], [6.31, 4.62]])
tux124 = bezCurve([[6.31, 4.62], [6.39, 4.67], [6.42, 4.69], [6.44, 4.72]])
tux125 = bezCurve([[6.44, 4.72], [6.44, 4.72], [6.44, 4.72], [6.44, 4.72]])
tux126 = [POLYLINE([[6.44, 4.72], [6.44, 4.72]])]
tux127 = bezCurve([[6.44, 4.72], [6.56, 4.83], [6.75, 5.04], [7.04, 5.14]])
tux128 = bezCurve([[7.04, 5.14], [7.14, 5.17], [7.25, 5.19], [7.37, 5.19]])
tux129 = [POLYLINE([[7.37, 5.19], [7.37, 5.19]])]
tux130 = bezCurve([[9.03, 4.21], [8.93, 4.21], [8.82, 4.15], [8.7, 4.08]])
tux131 = bezCurve([[8.7, 4.08], [8.58, 4.01], [8.43, 3.93], [8.28, 3.84]])
tux132 = bezCurve([[8.28, 3.84], [7.98, 3.66], [7.63, 3.49], [7.28, 3.49]])
tux133 = bezCurve([[7.28, 3.49], [6.93, 3.49], [6.65, 3.65], [6.44, 3.82]])
tux134 = bezCurve([[6.44, 3.82], [6.34, 3.9], [6.25, 3.99], [6.18, 4.05]])
tux135 = bezCurve([[6.18, 4.05], [6.15, 4.08], [6.12, 4.11], [6.09, 4.13]])
tux136 = bezCurve([[6.09, 4.13], [6.06, 4.15], [6.04, 4.17], [5.99, 4.17]])
tux137 = [POLYLINE([[5.99, 4.17], [5.99, 4.08]])]
tux138 = bezCurve([[5.99, 4.08], [5.99, 4.04], [5.99, 4.04], [5.99, 4.04]])
tux139 = bezCurve([[5.99, 4.04], [5.99, 4.04], [6.0, 4.04], [6.01, 4.03]])
tux140 = bezCurve([[6.01, 4.03], [6.03, 4.01], [6.06, 3.99], [6.09, 3.96]])
tux141 = bezCurve([[6.09, 3.96], [6.16, 3.89], [6.25, 3.81], [6.36, 3.72]])
tux142 = bezCurve([[6.36, 3.72], [6.58, 3.54], [6.89, 3.36], [7.28, 3.36]])
tux143 = bezCurve([[7.28, 3.36], [7.67, 3.36], [8.04, 3.55], [8.35, 3.72]])
tux144 = bezCurve([[8.35, 3.72], [8.5, 3.81], [8.64, 3.9], [8.76, 3.97]])
tux145 = bezCurve([[8.76, 3.97], [8.88, 4.04], [8.98, 4.08], [9.04, 4.08]])
tux146 = [POLYLINE([[9.04, 4.08], [9.03, 4.21]])]
tux147 = [POLYLINE([[9.03, 4.21], [9.03, 4.21]])]
tux148 = bezCurve([[9.38, 3.75], [9.64, 2.73], [10.24, 1.26], [10.62, 0.54]])
tux149 = bezCurve([[10.62, 0.54], [10.83, 0.16], [11.24, -0.65], [11.41, -1.63]])
tux150 = bezCurve([[11.41, -1.63], [11.53, -1.62], [11.65, -1.64], [11.78, -1.67]])
tux151 = bezCurve([[11.78, -1.67], [12.24, -0.48], [11.39, 0.81], [11.0, 1.17]])
tux152 = bezCurve([[11.0, 1.17], [10.84, 1.32], [10.83, 1.39], [10.91, 1.39]])
tux153 = bezCurve([[10.91, 1.39], [11.33, 1.02], [11.89, 0.26], [12.09, -0.59]])
tux154 = bezCurve([[12.09, -0.59], [12.18, -0.97], [12.2, -1.38], [12.1, -1.78]])
tux155 = bezCurve([[12.1, -1.78], [12.15, -1.8], [12.2, -1.82], [12.25, -1.85]])
tux156 = bezCurve([[12.25, -1.85], [12.99, -2.21], [13.27, -2.52], [13.13, -2.95]])
tux157 = bezCurve([[13.13, -2.95], [13.09, -2.95], [13.05, -2.95], [13.01, -2.95]])
tux158 = bezCurve([[13.01, -2.95], [13.0, -2.95], [13.0, -2.95], [12.99, -2.95]])
tux159 = bezCurve([[12.99, -2.95], [13.1, -2.61], [12.86, -2.36], [12.23, -2.07]])
tux160 = bezCurve([[12.23, -2.07], [11.57, -1.79], [11.05, -1.81], [10.96, -2.4]])
tux161 = bezCurve([[10.96, -2.4], [10.96, -2.43], [10.95, -2.46], [10.95, -2.49]])
tux162 = bezCurve([[10.95, -2.49], [10.9, -2.51], [10.85, -2.53], [10.8, -2.56]])
tux163 = bezCurve([[10.8, -2.56], [10.49, -2.73], [10.32, -3.03], [10.23, -3.41]])
tux164 = bezCurve([[10.23, -3.41], [10.14, -3.79], [10.11, -4.24], [10.08, -4.75]])
tux165 = bezCurve([[10.08, -4.75], [10.08, -4.75], [10.08, -4.75], [10.08, -4.75]])
tux166 = bezCurve([[10.08, -4.75], [10.07, -5.0], [9.96, -5.35], [9.86, -5.72]])
tux167 = bezCurve([[9.86, -5.72], [8.78, -6.49], [7.29, -6.82], [6.02, -5.95]])
tux168 = bezCurve([[6.02, -5.95], [5.93, -5.82], [5.84, -5.68], [5.73, -5.55]])
tux169 = bezCurve([[5.73, -5.55], [5.67, -5.46], [5.6, -5.38], [5.54, -5.3]])
tux170 = bezCurve([[5.54, -5.3], [5.67, -5.3], [5.78, -5.27], [5.87, -5.23]])
tux171 = bezCurve([[5.87, -5.23], [5.98, -5.18], [6.06, -5.1], [6.09, -5.0]])
tux172 = bezCurve([[6.09, -5.0], [6.17, -4.79], [6.09, -4.5], [5.85, -4.16]])
tux173 = bezCurve([[5.85, -4.16], [5.6, -3.83], [5.18, -3.45], [4.56, -3.07]])
tux174 = bezCurve([[4.56, -3.07], [4.56, -3.07], [4.56, -3.07], [4.56, -3.07]])
tux175 = bezCurve([[4.56, -3.07], [4.11, -2.79], [3.86, -2.45], [3.74, -2.07]])
tux176 = bezCurve([[3.74, -2.07], [3.62, -1.7], [3.64, -1.29], [3.73, -0.89]])
tux177 = bezCurve([[3.73, -0.89], [3.91, -0.12], [4.36, 0.62], [4.64, 1.09]])
tux178 = bezCurve([[4.64, 1.09], [4.72, 1.15], [4.67, 0.98], [4.35, 0.39]])
tux179 = bezCurve([[4.35, 0.39], [4.07, -0.15], [3.53, -1.39], [4.26, -2.37]])
tux180 = bezCurve([[4.26, -2.37], [4.28, -1.68], [4.45, -0.97], [4.73, -0.31]])
tux181 = bezCurve([[4.73, -0.31], [5.13, 0.61], [5.98, 2.2], [6.04, 3.47]])
tux182 = bezCurve([[6.04, 3.47], [6.08, 3.44], [6.2, 3.36], [6.25, 3.33]])
tux183 = bezCurve([[6.25, 3.33], [6.25, 3.33], [6.25, 3.33], [6.25, 3.33]])
tux184 = bezCurve([[6.25, 3.33], [6.41, 3.24], [6.52, 3.11], [6.67, 2.99]])
tux185 = bezCurve([[6.67, 2.99], [6.82, 2.86], [7.01, 2.76], [7.3, 2.74]])
tux186 = [POLYLINE([[7.3, 2.74], [7.3, 2.74]])]
tux187 = bezCurve([[7.3, 2.74], [7.63, 2.72], [7.89, 2.83], [8.09, 2.94]])
tux188 = bezCurve([[8.09, 2.94], [8.3, 3.06], [8.47, 3.19], [8.63, 3.25]])
tux189 = bezCurve([[8.63, 3.25], [8.63, 3.25], [8.63, 3.25], [8.63, 3.25]])
tux190 = bezCurve([[8.63, 3.25], [8.96, 3.35], [9.23, 3.53], [9.38, 3.75]])
tux191 = [POLYLINE([[9.38, 3.75], [9.38, 3.75]])]
tux192 = bezCurve([[11.49, -2.08], [11.62, -2.08], [11.79, -2.13], [11.97, -2.21]])
tux193 = bezCurve([[11.97, -2.21], [12.45, -2.43], [12.6, -2.62], [12.47, -2.9]])
tux194 = bezCurve([[12.47, -2.9], [12.36, -3.11], [11.88, -3.45], [11.56, -3.36]])
tux195 = bezCurve([[11.56, -3.36], [11.23, -3.27], [11.07, -2.8], [11.12, -2.44]])
tux196 = bezCurve([[11.12, -2.44], [11.15, -2.19], [11.29, -2.08], [11.49, -2.08]])
tux197 = [POLYLINE([[11.49, -2.08], [11.49, -2.08]])]
tux198 = bezCurve([[10.95, -2.74], [10.97, -3.18], [11.19, -3.63], [11.58, -3.73]])
tux199 = bezCurve([[11.58, -3.73], [12.0, -3.84], [12.61, -3.48], [12.86, -3.18]])
tux200 = bezCurve([[12.86, -3.18], [12.92, -3.18], [12.97, -3.18], [13.01, -3.18]])
tux201 = bezCurve([[13.01, -3.18], [13.24, -3.17], [13.43, -3.19], [13.62, -3.35]])
tux202 = [POLYLINE([[13.62, -3.35], [13.62, -3.35]])]
tux203 = [POLYLINE([[13.62, -3.35], [13.62, -3.35]])]
tux204 = bezCurve([[13.62, -3.35], [13.77, -3.48], [13.84, -3.72], [13.9, -3.98]])
tux205 = bezCurve([[13.9, -3.98], [13.96, -4.25], [14.01, -4.54], [14.2, -4.75]])
tux206 = [POLYLINE([[14.2, -4.75], [14.2, -4.75]])]
tux207 = [POLYLINE([[14.2, -4.75], [14.2, -4.75]])]
tux208 = bezCurve([[14.2, -4.75], [14.55, -5.14], [14.66, -5.4], [14.65, -5.57]])
tux209 = bezCurve([[14.65, -5.57], [14.64, -5.74], [14.52, -5.86], [14.29, -6.0]])
tux210 = bezCurve([[14.29, -6.0], [13.84, -6.27], [13.04, -6.51], [12.53, -7.13]])
tux211 = bezCurve([[12.53, -7.13], [12.09, -7.66], [11.55, -7.95], [11.07, -7.98]])
tux212 = bezCurve([[11.07, -7.98], [10.6, -8.02], [10.18, -7.82], [9.94, -7.34]])
tux213 = [POLYLINE([[9.94, -7.34], [9.94, -7.34]])]
tux214 = [POLYLINE([[9.94, -7.34], [9.94, -7.33]])]
tux215 = bezCurve([[9.94, -7.33], [9.79, -7.05], [9.85, -6.6], [9.98, -6.12]])
tux216 = bezCurve([[9.98, -6.12], [10.11, -5.65], [10.29, -5.16], [10.31, -4.76]])
tux217 = [POLYLINE([[10.31, -4.76], [10.31, -4.76]])]
tux218 = [POLYLINE([[10.31, -4.76], [10.31, -4.76]])]
tux219 = bezCurve([[10.31, -4.76], [10.34, -4.25], [10.37, -3.81], [10.45, -3.46]])
tux220 = bezCurve([[10.45, -3.46], [10.54, -3.12], [10.67, -2.89], [10.91, -2.76]])
tux221 = bezCurve([[10.91, -2.76], [10.92, -2.75], [10.94, -2.75], [10.95, -2.74]])
tux222 = [POLYLINE([[10.95, -2.74], [10.95, -2.74]])]
tux223 = bezCurve([[3.2, -2.77], [3.24, -2.77], [3.28, -2.78], [3.32, -2.78]])
tux224 = bezCurve([[3.32, -2.78], [3.59, -2.82], [3.82, -3.01], [4.05, -3.32]])
tux225 = bezCurve([[4.05, -3.32], [4.27, -3.63], [4.49, -4.05], [4.7, -4.52]])
tux226 = [POLYLINE([[4.7, -4.52], [4.7, -4.52]])]
tux227 = [POLYLINE([[4.7, -4.52], [4.7, -4.52]])]
tux228 = bezCurve([[4.7, -4.52], [4.88, -4.88], [5.24, -5.28], [5.56, -5.69]])
tux229 = bezCurve([[5.56, -5.69], [5.87, -6.1], [6.11, -6.51], [6.08, -6.82]])
tux230 = [POLYLINE([[6.08, -6.82], [6.08, -6.82]])]
tux231 = [POLYLINE([[6.08, -6.82], [6.08, -6.82]])]
tux232 = bezCurve([[6.08, -6.82], [6.04, -7.36], [5.74, -7.65], [5.27, -7.76]])
tux233 = bezCurve([[5.27, -7.76], [4.81, -7.86], [4.18, -7.76], [3.55, -7.43]])
tux234 = bezCurve([[3.55, -7.43], [3.55, -7.43], [3.55, -7.43], [3.55, -7.43]])
tux235 = bezCurve([[3.55, -7.43], [2.86, -7.06], [2.04, -7.1], [1.51, -6.99]])
tux236 = bezCurve([[1.51, -6.99], [1.24, -6.93], [1.07, -6.85], [0.99, -6.69]])
tux237 = bezCurve([[0.99, -6.69], [0.91, -6.54], [0.91, -6.27], [1.08, -5.81]])
tux238 = [POLYLINE([[1.08, -5.81], [1.08, -5.81]])]
tux239 = [POLYLINE([[1.08, -5.81], [1.08, -5.81]])]
tux240 = bezCurve([[1.08, -5.81], [1.16, -5.55], [1.1, -5.27], [1.06, -5.0]])
tux241 = bezCurve([[1.06, -5.0], [1.02, -4.74], [1.0, -4.5], [1.09, -4.33]])
tux242 = [POLYLINE([[1.09, -4.33], [1.09, -4.33]])]
tux243 = [POLYLINE([[1.09, -4.33], [1.09, -4.33]])]
tux244 = bezCurve([[1.09, -4.33], [1.21, -4.11], [1.37, -4.03], [1.58, -3.95]])
tux245 = bezCurve([[1.58, -3.95], [1.79, -3.88], [2.04, -3.82], [2.24, -3.62]])
tux246 = [POLYLINE([[2.24, -3.62], [2.24, -3.62]])]
tux247 = [POLYLINE([[2.24, -3.62], [2.24, -3.62]])]
tux248 = bezCurve([[2.24, -3.62], [2.43, -3.43], [2.56, -3.19], [2.72, -3.02]])
tux249 = bezCurve([[2.72, -3.02], [2.86, -2.87], [2.99, -2.78], [3.2, -2.78]])
tux250 = bezCurve([[3.2, -2.78], [3.2, -2.77], [3.2, -2.77], [3.2, -2.77]])
tux251 = [POLYLINE([[3.2, -2.77], [3.2, -2.77]])]
tux = STRUCT(tux1+tux2+tux3+tux4+tux5+tux6+tux7+tux8+tux9+tux10+tux11+tux12+tux13+tux14+
	tux15+tux16+tux17+tux18+tux19+tux20+tux21+tux22+tux23+tux24+tux25+tux26+tux27+tux28+
	tux29+tux30+tux31+tux32+tux33+tux34+tux35+tux36+tux37+tux38+tux39+tux40+tux41+tux42+
	tux43+tux44+tux45+tux46+tux47+tux48+tux49+tux50+tux51+tux52+tux53+tux54+tux55+tux56+
	tux57+tux58+tux59+tux60+tux61+tux62+tux63+tux64+tux65+tux66+tux67+tux68+tux69+tux70+
	tux71+tux72+tux73+tux74+tux75+tux76+tux77+tux78+tux79+tux80+tux81+tux82+tux83+tux84+
	tux85+tux86+tux87+tux88+tux89+tux90+tux91+tux92+tux93+tux94+tux95+tux96+tux97+tux98+
	tux99+tux100+tux101+tux102+tux103+tux104+tux105+tux106+tux107+tux108+tux109+tux110+
	tux111+tux112+tux113+tux114+tux115+tux116+tux117+tux118+tux119+tux120+tux121+tux122+
	tux123+tux124+tux125+tux126+tux127+tux128+tux129+tux130+tux131+tux132+tux133+tux134+
	tux135+tux136+tux137+tux138+tux139+tux140+tux141+tux142+tux143+tux144+tux145+tux146+
	tux147+tux148+tux149+tux150+tux151+tux152+tux153+tux154+tux155+tux156+tux157+tux158+
	tux159+tux160+tux161+tux162+tux163+tux164+tux165+tux166+tux167+tux168+tux169+tux170+
	tux171+tux172+tux173+tux174+tux175+tux176+tux177+tux178+tux179+tux180+tux181+tux182+
	tux183+tux184+tux185+tux186+tux187+tux188+tux189+tux190+tux191+tux192+tux193+tux194+
	tux195+tux196+tux197+tux198+tux199+tux200+tux201+tux202+tux203+tux204+tux205+tux206+
	tux207+tux208+tux209+tux210+tux211+tux212+tux213+tux214+tux215+tux216+tux217+tux218+
	tux219+tux220+tux221+tux222+tux223+tux224+tux225+tux226+tux227+tux228+tux229+tux230+
	tux231+tux232+tux233+tux234+tux235+tux236+tux237+tux238+tux239+tux240+tux241+tux242+
	tux243+tux244+tux245+tux246+tux247+tux248+tux249+tux250+tux251)
tux = COLOR(P_DGREEN)(PROD([OFFSET([0.15,0.15])(tux),Q(0.7)]))

# FULL SCENE

full_scene = STRUCT([
	T([1,2,3])([-10,-5,-0.5])(grass),
	full_building,
	T([1,2,3])([66.5,28.8,0.1])(S([1,2,3])([4.5,4.5,4.5])(glass)),
	T([1,2])([40,40])(fountain_and_water),
	T([1,2])([5,40])(fountain_and_water),
	T([1,2])([2,25])(STRUCT(NN(6)([pot,T(1)(8)]))),
	T([1,2,3])([30,40,0])(R([1,2])(PI)(tux))
	])

VIEW(full_scene)