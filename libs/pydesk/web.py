
class Web(RenderLib):

    def __init__(self):
        super().__init__()
        self.stl = WebRenderer()
        )

    def _renderTextObj(self, aText, aHeightPx):
        pnt = gp_Pnt(0, 0, 0).Transformed(self.aMove.getTrsf())
        color = self.aStyle.getNormedColor(),
        self.web.drawLabel(pnt, aText, color)

    def _renderShapeObj(self, aShape):
        shapeTr = BRepBuilderAPI_Transform(aShape, self.aMove.getTrsf()).Shape()
        color = self.aStyle.getNormedColor()
        transparency = self.aStyle.getNormedTransparency()
        self.web.drawShape(shapeTr, color, transparency)

    def _renderWireObj(self, aWire, aWireRadius):
        startPoint, tangentDir = _getWireStartPointAndTangentDir(aWire)
        profileCircle = GC_MakeCircle(startPoint, tangentDir, aWireRadius).Value()
        profileEdge = BRepBuilderAPI_MakeEdge(profileCircle).Edge()
        profileWire = BRepBuilderAPI_MakeWire(profileEdge).Wire()

        shape = BRepOffsetAPI_MakePipe(aWire, profileWire).Shape()

        self._renderShapeObj(shape)

    def renderLabel(self, aText, aHeightPx):
        self._renderTextObj(aText, aHeightPx)

    def renderBox(self, aSizeX, aSizeY, aSizeZ):
        shape = BRepPrimAPI_MakeBox(aSizeX, aSizeY, aSizeZ).Shape()
        self._renderShapeObj(shape)

    def renderSphere(self, aRadius):
        shape = BRepPrimAPI_MakeSphere(aRadius).Shape()
        self._renderShapeObj(shape)

    def renderCone(self, aRadius1, aRadius2, aHeight):
        shape = BRepPrimAPI_MakeCone(aRadius1, aRadius2, aHeight).Shape()
        self._renderShapeObj(shape)

    def renderCylinder(self, aRadius, aHeight):
        shape = BRepPrimAPI_MakeCylinder(aRadius, aHeight).Shape()
        self._renderShapeObj(shape)

    def renderTorus(self, aRadius1, aRadius2):
        shape = BRepPrimAPI_MakeTorus(aRadius1, aRadius2).Shape()
        self._renderShapeObj(shape)

    def renderCircle(self, aPnt1, aPnt2, aPnt3, aLineWidth):
        geomCircle = GC_MakeCircle(aPnt1, aPnt2, aPnt3).Value()
        wire = BRepBuilderAPI_MakeEdge(geomCircle).Edge()
        self._renderWireObj(wire, aLineWidth)

    def renderWire(self, aWire, aWireRadius):
        self._renderWireObj(aWire, aWireRadius)

    def renderSurface(self, aSurface):
        self._renderShapeObj(aSurface)
