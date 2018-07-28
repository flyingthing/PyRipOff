# original author - Ian Mallett
# graciously allowed the use of this code ( - Kochanek-Bartels Spline - 1.0.0 - May 2008) under the GPL

class Spline():
    def __init__(self):
        self.c = 0
        self.b = 0
        self.t = 0
        self.ControlPoints = []

    def wayPoints(self):
        c = self.c
        b = self.b
        t = self.t
        ControlPoints = self.ControlPoints

        ControlPoints = ControlPoints + ControlPoints[0:2]

        tans = []
        tand = []

        for x in range(len(ControlPoints) - 2):
            tans.append([])
            tand.append([])

        cona = (1 - t) * (1 + b) * (1 - c) * 0.5
        conb = (1 - t) * (1 - b) * (1 + c) * 0.5
        conc = (1 - t) * (1 + b) * (1 + c) * 0.5
        cond = (1 - t) * (1 - b) * (1 - c) * 0.5

        i = 1

        while i < len(ControlPoints) - 1:
            pa = ControlPoints[i - 1]
            pb = ControlPoints[i]
            pc = ControlPoints[i + 1]
            x1 = pb[0] - pa[0]
            y1 = pb[1] - pa[1]

            x2 = pc[0] - pb[0]
            y2 = pc[1] - pb[1]

            tans[i - 1] = (cona * x1 + conb * x2, cona * y1 + conb * y2)
            tand[i - 1] = (conc * x1 + cond * x2, conc * y1 + cond * y2)

            i += 1


        t_inc = 0.2
        i = 1
        finalLines = []

        while i < len(ControlPoints) - 2:
            p0 = ControlPoints[i]
            p1 = ControlPoints[i + 1]
            m0 = tand[i - 1]
            m1 = tans[i]

            # curve from p0 to p1
            Lines = [(p0[0], p0[1])]
            t_iter = t_inc

            while t_iter < 1.0:
                h00 = (2 * (t_iter ** 3)) - (3 * (t_iter ** 2)) + 1
                h10 = (1 * (t_iter ** 3)) - (2 * (t_iter ** 2)) + t_iter
                h01 = (-2 * (t_iter ** 3)) + (3 * (t_iter ** 2))
                h11 = (1 * (t_iter ** 3)) - (1 * (t_iter ** 2))
                px = h00 * p0[0] + h10 * m0[0] + h01 * p1[0] + h11 * m1[0]
                py = h00 * p0[1] + h10 * m0[1] + h01 * p1[1] + h11 * m1[1]

                Lines.append((px, py))
                t_iter += t_inc

            Lines.append((p1[0], p1[1]))
            Lines2 = []

            for p in Lines:
                Lines2.append((int(round(p[0])), int(round(p[1]))))

            finalLines.extend(Lines2)
            i += 1

        return finalLines
