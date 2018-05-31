
def cell_is_deletable(nb, index):
    JS = 'return Jupyter.notebook.get_cell({}).is_deletable();'.format(index)
    return nb.browser.execute_script(JS)

def remove_cells(notebook):
    for i in notebook.cells:
        notebook.delete_cell(notebook.index(i))

def test_delete_cells(notebook):
    a = 'print("a")'
    b = 'print("b")'
    c = 'print("c")'

    notebook.edit_cell(index=0, content=a)
    notebook.append(b, c)
    notebook.to_command_mode()
    
    # Validate initial state
    assert notebook.get_cells_contents() == [a, b, c]
    for cell in range(0, 3):
        assert cell_is_deletable(notebook, cell)

    notebook.set_cell_metadata(0, 'deletable', 'false')
    notebook.set_cell_metadata(1, 'deletable', 0
    )   
    assert not cell_is_deletable(notebook, 0)
    assert cell_is_deletable(notebook, 1)
    assert cell_is_deletable(notebook, 2)
    
    # Try to delete cell a (should not be deleted)
    notebook.delete_cell(0)
    assert notebook.get_cells_contents() == [a, b, c]

    # Try to delete cell b (should succeed)
    notebook.delete_cell(1)
    assert notebook.get_cells_contents() == [a, c]

    # Try to delete cell c (should succeed)
    notebook.delete_cell(1)
    assert notebook.get_cells_contents() == [a]

    # Change the deletable state of cell a
    notebook.set_cell_metadata(0, 'deletable', 'true')

    # Try to delete cell a (should succeed)
    notebook.delete_cell(0)
    assert len(notebook.cells) == 1 # it contains an empty cell

    # Make sure copied cells are deletable
    notebook.edit_cell(index=0, content=a)
    notebook.set_cell_metadata(0, 'deletable', 'false')
    assert not cell_is_deletable(notebook, 0)
    notebook.to_command_mode()
    notebook.current_cell.send_keys('cv')
    assert len(notebook.cells) == 2
    assert cell_is_deletable(notebook, 1)

    remove_cells(notebook)
    assert len(notebook.cells) == 1    # notebook should create one automatically on empty notebook
