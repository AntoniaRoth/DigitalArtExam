import turtle as t
import math
import time
from tkinter import *
from tkinter import simpledialog, messagebox, colorchooser
import copy
from PIL import ImageGrab


def draw_everything():
    global new_polygons
    t.tracer(0)
    all_polygons.append(copy.deepcopy(current_polygons))
    for polygon in new_polygons:
        try:
            color = polygon[2]
            t.color(color)
            fill = polygon[1]
            if fill:
                t.begin_fill()
            polygon = polygon[0]
            t.penup()
            t.goto(polygon[0][0] / polygon[0][2], polygon[0][1] / polygon[0][2])
            t.pendown()
            for cor in polygon:
                t.goto(cor[0] / cor[2], cor[1] / cor[2])
            t.end_fill()
        except:
            continue

        current_polygons.append([polygon, fill, color])
    new_polygons = []
    t.update()
    start_screen_func()


def get_point_func(wanted, window):
    global point_x, point_y
    point_x_lbl = Label(window, text=f"Gib den {wanted[0]} Ihres {wanted[2]}.")
    point_x_entry = Entry(window)
    point_y_lbl = Label(window, text=f"Gib den {wanted[1]} Ihres {wanted[2]}.")
    point_y_entry = Entry(window)
    point_x_lbl.pack()
    point_x_entry.pack()
    point_y_lbl.pack()
    point_y_entry.pack()


def calculate_circle_points(x_center, y_center, radius, num_points):
    circle_points = []

    for i in range(num_points):
        angle = 2 * math.pi * i / num_points
        x = x_center + radius * math.cos(angle)
        y = y_center + radius * math.sin(angle)
        circle_points.append((x, y, 1))
    circle_points.append((x_center + radius, y_center, 1))
    return circle_points


def create_poly_points_func(win, shape, fill):
    vals = []
    for i in win.winfo_children():
        if type(i).__name__ == "Entry":
            vals.append(i.get())
    if "" in vals:
        messagebox.showerror("Ungültige Eingabe", "Jedes Feld muss einen Wert haben.")
    else:
        vals = list(map(int, vals))
        if shape == "c":
            new_polygons.append([calculate_circle_points(vals[0], vals[1], vals[2], 100), fill.get(), drawing_color])
        elif shape == "r":
            new_polygons.append([[(vals[0], vals[1], 1), (vals[0] + vals[2], vals[1], 1), (vals[0] + vals[2], vals[1] + vals[3], 1), (vals[0], vals[1] + vals[3], 1), (vals[0], vals[1], 1)], fill.get(), drawing_color])
        elif shape == "p":
            polygon = []
            for i in range(int(len(vals)/2)):
                polygon.append((vals[i], vals[i + 1], 1))
            polygon.append((vals[0], vals[1], 1))
            new_polygons.append([polygon, fill.get(), drawing_color])
        win.destroy()
        draw_everything()


def select_color_func():
    global drawing_color
    drawing_color = colorchooser.askcolor()[1]


def new_shape_func():
    shape = simpledialog.askstring("Form definieren", "Schreiben Sie 'r' für ein Rechteck, 'c' für einen Kreis, \n"
                                                       "'p' für ein Polygon mit einer bestimmten Anzahl von Ecken.\n")
    while True:
        if shape in ["c", "r", "p", None]:
            break
        shape = simpledialog.askstring("Form definieren", "Schreiben Sie 'r' für ein Rechteck, 'c' für einen Kreis, \n"
                                                       "'p' für ein Polygon mit einer bestimmten Anzahl von Ecken.\n")
    shape_win = Toplevel()
    fill_var = IntVar()
    fill_btn = Checkbutton(shape_win, text="Füllen", variable=fill_var, onvalue=True, offvalue=False)
    fill_btn.pack()
    color_btn = Button(shape_win, text="Farbe wählen", command=select_color_func)
    color_btn.pack()
    if shape == "c":
        get_point_func(["x-Koordinate", "y-Koordinate", "Mittelpunkt"], shape_win)
        radius_lbl = Label(shape_win, text="Gib den Radius ein:")
        radius_entry = Entry(shape_win)
        radius_lbl.pack()
        radius_entry.pack()

    elif shape == "r":
        get_point_func(["x-Koordinate", "y-Koordinate", "linke untere Ecke"], shape_win)
        get_point_func(["Breite", "Höhe", "Rechteck"], shape_win)

    elif shape == "p":
        while True:
            corners = simpledialog.askinteger("Ecken", "Geben Sie die Anzahl der Ecken an, die Ihr Polygon haben soll.(zwischen 1 und 8)\n")
            if corners is None or 0 < int(corners) < 9:
                break

        if corners is not None:
            for i in range(int(corners)):
                get_point_func(["x-Koordinate", "y-Koordinate", f"{i+1} Ecken"], shape_win)

    submit_btn = Button(shape_win, text="Los", command=lambda: create_poly_points_func(shape_win, shape, fill_var))
    submit_btn.pack()
    shape_win.mainloop()


def translate_matrix_func(vector):
    return [[1, 0, vector[0]], [0, 1, vector[1]], [0, 0, 1]]


def rotate_matrix_func(angle):
    cos_angle = math.cos(angle)
    sin_angle = math.sin(angle)
    return [[cos_angle, -sin_angle, 0], [sin_angle, cos_angle, 0], [0, 0, 1]]


def scale_matrix_func(factor):
    return [[factor[0], 0, 0], [0, factor[1], 0], [0, 0, 1]]


def shear_matrix_func(x_shear, y_shear):
    return [[1, x_shear, 0], [y_shear, 1, 0], [0, 0, 1]]


def mirror_matrix_func(mirror_line_point1, mirror_line_point2):
    a = mirror_line_point2[1] - mirror_line_point1[1]
    b = mirror_line_point1[0] - mirror_line_point2[0]
    c = mirror_line_point2[0] * mirror_line_point1[1] - mirror_line_point1[0] * mirror_line_point2[1]
    return [[1 - 2 * a ** 2 / (a ** 2 + b ** 2), -2 * a * b / (a ** 2 + b ** 2), -2 * a * c / (a ** 2 + b ** 2)],
            [-2 * a * b / (a ** 2 + b ** 2), 1 - 2 * b ** 2 / (a ** 2 + b ** 2), -2 * b * c / (a ** 2 + b ** 2)],
            [0, 0, 1]]


def translate_func(pattern, translation=None, repetitions=1):
    if translation is None:
        x_com = simpledialog.askinteger("Übersetzungsvektor", "Gib die x-Komponente deines Vektors an.")
        y_com = simpledialog.askinteger("Übersetzungsvektor", "Gib die y-Komponente deines Vektors an.")
        translation = (x_com, y_com, 1)

    if None not in translation:
        if not pattern:
            translation_matrix = translate_matrix_func(translation)
            transformed_polygons = []

            for polygon in current_polygons:
                new_polygon = [transform_point_func(point, translation_matrix) for point in polygon[0]]
                transformed_polygons.append([new_polygon, polygon[1], polygon[2]])

            new_polygons.extend(transformed_polygons)
            if repetitions != 1:
                for i in range(repetitions):
                    for polygon in transformed_polygons:
                        transformed_polygons2 = []
                        new_polygon = [transform_point_func(point, translation_matrix) for point in new_polygons[-len(transformed_polygons)][0]]
                        transformed_polygons2.append([new_polygon, polygon[1], polygon[2]])

                        new_polygons.extend(transformed_polygons2)

        return translation


def rotate_func(pattern, origin=None, angle=None, repetitions=1):
    if origin is None:
        x_com = simpledialog.askinteger("Rotationspunkt", "Geben Sie die x-Koordinate Ihres Rotationspunktes an.")
        y_com = simpledialog.askinteger("Rotationspunkt", "Geben Sie die y-Koordinate Ihres Rotationspunktes an.")
        origin = (x_com, y_com, 1)

    if None not in origin:
        if angle is None:
            angle = simpledialog.askinteger("Winkel definieren", "Geben Sie den Winkel (in Grad) ein, um die Zeichnung zu drehen.")
        if angle is not None:
            if not pattern:
                angle = math.radians(angle)
                rotation_matrix = rotate_matrix_func(angle)
                transformed_polygons = []
                for polygon in current_polygons:
                    new_polygon = [transform_point_func(point, translate_matrix_func((-origin[0], -origin[1]))) for point in
                                   polygon[0]]
                    new_polygon = [transform_point_func(point, rotation_matrix) for point in new_polygon]
                    new_polygon = [transform_point_func(point, translate_matrix_func((origin[0], origin[1]))) for point in
                                   new_polygon]
                    transformed_polygons.append([new_polygon, polygon[1], polygon[2]])

                new_polygons.extend(transformed_polygons)
                if repetitions != 1:
                    for i in range(repetitions):
                        for polygon in transformed_polygons:
                            transformed_polygons2 = []
                            new_polygon = [transform_point_func(point, translate_matrix_func((-origin[0], -origin[1])))
                                           for point in new_polygons[-len(transformed_polygons)][0]]
                            new_polygon = [transform_point_func(point, rotation_matrix) for point in new_polygon]
                            new_polygon = [transform_point_func(point, translate_matrix_func((origin[0], origin[1])))
                                           for point in new_polygon]
                            transformed_polygons2.append([new_polygon, polygon[1], polygon[2]])

                            new_polygons.extend(transformed_polygons2)
            return origin, angle


def scale_func(pattern, factor=None, origin=None, repetitions=1):
    if factor is None:
        x_com = simpledialog.askinteger("Skalierungsfaktor", "Geben Sie den x-Faktor Ihrer Skalierung an.")
        y_com = simpledialog.askinteger("Skalierungsfaktor", "Geben Sie den y-Faktor Ihrer Skalierung an.")
        factor = (x_com, y_com, 1)

    if None not in factor:
        if origin is None:
            x_com = simpledialog.askinteger("Skalierungspunkt", "Geben Sie die x-Koordinate Ihres Skalierungspunktes an.")
            y_com = simpledialog.askinteger("Skalierungspunkt", "Geben Sie die y-Koordinate Ihres Skalierungspunktes an.")
            origin = (x_com, y_com, 1)

        if None not in origin:
            if not pattern:
                scaling_matrix = scale_matrix_func(factor)
                transformed_polygons = []
                for polygon in current_polygons:
                    new_polygon = [transform_point_func(point, translate_matrix_func((-origin[0], -origin[1]))) for point in
                                   polygon[0]]
                    new_polygon = [transform_point_func(point, scaling_matrix) for point in new_polygon]
                    new_polygon = [transform_point_func(point, translate_matrix_func((origin[0], origin[1]))) for point in
                                   new_polygon]
                    transformed_polygons.append([new_polygon, polygon[1], polygon[2]])

                new_polygons.extend(transformed_polygons)
                if repetitions != 1:
                    for i in range(repetitions):
                        for polygon in transformed_polygons:
                            transformed_polygons2 = []
                            new_polygon = [transform_point_func(point, translate_matrix_func((-origin[0], -origin[1])))
                                           for point in new_polygons[-len(transformed_polygons)][0]]
                            new_polygon = [transform_point_func(point, scaling_matrix) for point in new_polygon]
                            new_polygon = [transform_point_func(point, translate_matrix_func((origin[0], origin[1])))
                                           for point in new_polygon]

                            transformed_polygons2.append([new_polygon, polygon[1], polygon[2]])
                            new_polygons.extend(transformed_polygons2)

            return factor, origin


def shear_func(pattern, shear=None, repetitions=1):
    if shear is None:
        x_com = simpledialog.askinteger("Scherwerte", "Geben Sie den x-Scherfaktor Ihrer Scherung an.")
        y_com = simpledialog.askinteger("Scherwerte", "Geben Sie den y-Scherfaktor Ihrer Scherung an.")
        shear = (x_com, y_com, 1)

    if None not in shear:
        if not pattern:
            shear_matrix = shear_matrix_func(shear[0], shear[1])
            transformed_polygons = []
            for polygon in current_polygons:
                new_polygon = [transform_point_func(point, shear_matrix) for point in polygon[0]]
                transformed_polygons.append([new_polygon, polygon[1], polygon[2]])

            new_polygons.extend(transformed_polygons)

            if repetitions != 1:
                for i in range(repetitions):
                    for polygon in transformed_polygons:
                        transformed_polygons2 = []
                        new_polygon = [transform_point_func(point, shear_matrix) for point in new_polygons[-len(transformed_polygons)][0]]

                        transformed_polygons2.append([new_polygon, polygon[1], polygon[2]])
                        new_polygons.extend(transformed_polygons2)
        return shear


def mirror_func(pattern, point1=None, point2=None, repetitions=1):
    if point1 is None:
        x_com = simpledialog.askinteger("Erster Spiegelpunkt", "Geben Sie die x-Koordinate Ihres erster Spiegelpunktes an.")
        y_com = simpledialog.askinteger("Erster Spiegelpunkt", "Geben Sie die x-Koordinate Ihres erster Spiegelpunktes an.")
        point1 = (x_com, y_com, 1)

    if None not in point1:
        if point2 is None:
            x_com = simpledialog.askinteger("Zweiter Spiegelpunkt", "Geben Sie die x-Koordinate Ihres zweiten Spiegelpunktes an.")
            y_com = simpledialog.askinteger("Zweiter Spiegelpunkt", "Geben Sie die y-Koordinate Ihres zweiten Spiegelpunktes an.")
            point2 = (x_com, y_com, 1)

        if None not in point2:
            if not pattern:
                mirror_matrix = mirror_matrix_func(point1, point2)
                transformed_polygons = []
                for polygon in current_polygons:
                    new_polygon = [transform_point_func(point, mirror_matrix) for point in polygon[0]]
                    transformed_polygons.append([new_polygon, polygon[1], polygon[2]])

                new_polygons.extend(transformed_polygons)

                if repetitions != 1:
                    for i in range(repetitions):
                        for polygon in transformed_polygons:
                            transformed_polygons2 = []
                            new_polygon = [transform_point_func(point, mirror_matrix) for point in new_polygons[-len(transformed_polygons)][0]]

                            transformed_polygons2.append([new_polygon, polygon[1], polygon[2]])
                            new_polygons.extend(transformed_polygons2)

            return point1, point2


def transform_func(pattern=False):
    transformation = simpledialog.askinteger("Transformations-Eingabefehler",
                                                 "Schreiben Sie '1', um die Zeichnung zu übersetzen, '2', um die Zeichnung zu drehen,\n"
                                                 "'3', um die Zeichnung zu skalieren, '4', um die Zeichnung zu scheren,\n"
                                                 "'5', um die Zeichnung zu spiegeln.\n"
                                                 "Drücken Sie 'Abbrechen', um zurückzugehen.")
    while True:
        if transformation in [1, 2, 3, 4, 5, None]:
            break
        transformation = simpledialog.askinteger("Transformations-Eingabefehler",
                                                 "Schreiben Sie '1', um die Zeichnung zu übersetzen, '2', um die Zeichnung zu drehen,\n"
                                                 "'3', um die Zeichnung zu skalieren, '4', um die Zeichnung zu scheren,\n"
                                                 "'5', um die Zeichnung zu spiegeln.\n"
                                                 "Drücken Sie 'Abbrechen', um zurückzugehen.")

    if transformation == 1:
        res = translate_func(pattern)

    elif transformation == 2:
        res = rotate_func(pattern)

    elif transformation == 3:
        res = scale_func(pattern)

    elif transformation == 4:
        res = shear_func(pattern)

    elif transformation == 5:
        res = mirror_func(pattern)

    elif transformation is None:
        res = None

    if pattern:
        return [transformation, res]
    else:
        draw_everything()


def transform_point_func(point, transformation_matrix):
    x = point[0]
    y = point[1]
    w = point[2]
    new_x = x * transformation_matrix[0][0] + y * transformation_matrix[0][1] + w * transformation_matrix[0][2]
    new_y = x * transformation_matrix[1][0] + y * transformation_matrix[1][1] + w * transformation_matrix[1][2]
    new_w = x * transformation_matrix[2][0] + y * transformation_matrix[2][1] + w * transformation_matrix[2][2]
    return new_x, new_y, new_w


def create_new_pattern_func():
    new_pattern = []
    while True:
        pattern = transform_func(True)
        if pattern[0] is None:
            break
        repetitions = simpledialog.askinteger("Wiederholungen", "Wie oft sollte diese Umwandlung durchgeführt werden?\n")
        if repetitions is None:
            break
        if repetitions is not None:
            pattern.append(int(repetitions))
            new_pattern.append(pattern)
    if new_pattern:
        all_patterns.append(new_pattern)


def use_pattern_func():
    transformations_list = ["Verschieben", "Rotieren", "Skalieren", "Scheren", "Spiegeln"]
    actions = []
    for pattern in all_patterns:
        action = ""
        for transformation in pattern:
            text = f"{transformations_list[int(transformation[0])-1]} {transformation[2]} Mal"
            action += text + ", "
        actions.append(action)
    pattern_text = "".join(f"'{index}' to {obj}\n" for index, obj in enumerate(actions))
    pattern = simpledialog.askinteger("Wähle das Muster", "Schreibe\n" + pattern_text +
                                      "Drücke 'Cancel' zum zurück gehen.")

    if pattern is not None:
        current_pattern = all_patterns[int(pattern)]
        for transformation in current_pattern:
            if transformation[0] == 1:
                res = translate_func(False, transformation[1], transformation[2])

            elif transformation[0] == 2:
                res = rotate_func(False, transformation[1][0], transformation[1][1], transformation[2])

            elif transformation[0] == 3:
                res = scale_func(False, transformation[1][0], transformation[1][1], transformation[2])

            elif transformation[0] == 4:
                res = shear_func(False, transformation[1], transformation[2])

            elif transformation[0] == 5:
                res = mirror_func(False, transformation[1][0], transformation[1][1], transformation[2])
        draw_everything()


def pattern_func():
    pattern = simpledialog.askstring("Fehler bei der Mustereingabe", "Schreiben Sie 'n', um ein neues Muster zu erstellen, 'p', um eines Ihrer vorhandenen Muster zu verwenden."
                                                     "Drücken Sie 'Abbrechen', um zurückzugehen.")
    while True:
        if pattern in ["n", "p", None]:
            break
        pattern = simpledialog.askstring("Fehler bei der Mustereingabe", "Schreiben Sie 'n', um ein neues Muster zu erstellen, 'p', um eines Ihrer vorhandenen Muster zu verwenden."
                                                     "Drücken Sie 'Abbrechen', um zurückzugehen.")
    if pattern == "n":
        create_new_pattern_func()
    elif pattern == "p":
        use_pattern_func()
    elif pattern is None:
        pass


def save_img_func():
    time.sleep(0.2)
    screen = t.getcanvas()
    x0, y0 = screen.winfo_rootx() + 110, screen.winfo_rooty() + 40
    x1, y1 = x0 + screen.winfo_width() + 180, y0 + screen.winfo_height() + 150
    image = ImageGrab.grab(bbox=(x0, y0, x1, y1))

    # Speichere das erfasste Bild als PNG
    image.save("turtle_screen.png", "PNG")


def one_step_back_func():
    global new_polygons, current_polygons
    t.clear()
    last_polygon = all_polygons.pop()
    current_polygons = []
    new_polygons = last_polygon
    draw_everything()


def start_screen_func():
    global current_polygons, new_polygons
    while True:
        what_to_do = simpledialog.askstring("Transformieren/Zeichnen", "Schreiben Sie 't', um die Zeichnung zu transformieren, 'c', um eine neue Zeichnung zu erstellen.\n"
                                                                  "'p', um ein Muster mit dem Polygon zu erstellen, "
                                                                  "'s', um die aktuelle Zeichnung zu speichern, \n"
                                                                  "'z', um einen Schritt zurück zu gehen oder "
                                                                  "d' um den gesamten Bildschirm zu löschen.\n")
        while True:
            if what_to_do in ["t", "c", "p", "s", "z", "d", None]:
                break
            what_to_do = simpledialog.askstring("Transformieren/Zeichnen", "Schreiben Sie 't', um die Zeichnung zu transformieren, 'c', um eine neue Zeichnung zu erstellen.\n"
                                                                  "'p', um ein Muster mit dem Polygon zu erstellen, "
                                                                  "'s', um die aktuelle Zeichnung zu speichern, \n"
                                                                  "'z', um einen Schritt zurück zu gehen oder "
                                                                  "d' um den gesamten Bildschirm zu löschen.\n")

        if what_to_do == "c":
            new_shape_func()
        elif what_to_do == "t":
            transform_func()
        elif what_to_do == "p":
            pattern_func()
        elif what_to_do == "s":
            save_img_func()
        elif what_to_do == "z":
            one_step_back_func()
        elif what_to_do == "d":
            new_polygons = []
            current_polygons = []
            t.clear()
        elif what_to_do is None:
            break


root = Tk()
root.withdraw()
drawing_color = "black"
all_patterns = []
t.hideturtle()
t.speed(0)
t.Screen().delay(0)
current_polygons = []
all_polygons = []
new_polygons = []
point_x, point_y = 0, 0

draw_everything()
start_screen_func()

root.mainloop()
