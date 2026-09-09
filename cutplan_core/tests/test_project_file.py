from cutplan_core import Design, Material, Part, Project, project_file


def test_saved_project_reopens_with_the_same_width(tmp_path):
    shelf = Design.bookshelf("B", 800, 1800, 300, 18, 4)
    sheet = Material.standard_sheet(45)
    path = tmp_path / "test.cutplan"

    project_file.save(path, Project(shelf, sheet))
    reopened = project_file.load(path)

    assert reopened.design.param("width") == 800


def test_saved_project_reopens_with_the_same_parts(tmp_path):
    shelf = Design.bookshelf("B", 800, 1800, 300, 18, 4)
    sheet = Material.standard_sheet(45)
    path = tmp_path / "test.cutplan"

    project_file.save(path, Project(shelf, sheet))
    reopened = project_file.load(path)

    assert len(reopened.design.build_parts()) == len(shelf.build_parts())


def test_saved_project_reopens_with_the_same_material(tmp_path):
    box = Design.box("X", 600, 400, 400, 12)
    sheet = Material(2000, 1000, 4, 60)
    path = tmp_path / "test.cutplan"

    project_file.save(path, Project(box, sheet))
    reopened = project_file.load(path)

    assert reopened.material == sheet


def test_custom_design_round_trips_through_json(tmp_path):
    custom = Design.custom("C", [Part("Shelf", 100, 200, 3), Part("Door", 400, 700, 1)])
    sheet = Material.standard_sheet(10)
    path = tmp_path / "custom.cutplan"

    project_file.save(path, Project(custom, sheet))
    reopened = project_file.load(path)

    assert reopened.design.build_parts() == custom.build_parts()


def test_saved_file_is_human_readable_json(tmp_path):
    shelf = Design.bookshelf("B", 800, 1800, 300, 18, 4)
    sheet = Material.standard_sheet(45)
    path = tmp_path / "test.cutplan"

    project_file.save(path, Project(shelf, sheet))

    text = path.read_text(encoding="utf-8")
    assert '"kind": "BOOKSHELF"' in text
    assert '"sheetWidth": 2440' in text
