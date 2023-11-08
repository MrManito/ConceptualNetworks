from StructureStemming import StructureStemming

def test_one():
    handleStemming = StructureStemming()
    handleStemming.add('educ', 'educacion')
    assert handleStemming.getStemWords() == {'educ': [{'educacion': 1}, 1]}

def test_two():
    handleStemming = StructureStemming()
    handleStemming.add('educ', 'educacion')
    handleStemming.add('educ', 'educacion')
    handleStemming.add('educ', 'educa')
    assert handleStemming.getStemWords() == {'educ': [{'educacion': 2, 'educa': 1}, 3]}

def test_three():
    handleStemming = StructureStemming()
    handleStemming.add('educ', 'educacion')
    handleStemming.add('educ', 'educacion')
    handleStemming.add('educ', 'educa')
    handleStemming.add('corr', 'correr')
    assert handleStemming.getStemWords() == {'educ': [{'educacion': 2, 'educa': 1}, 3], 'corr': [{'correr': 1}, 1]}

def test_four():
    # Prueba de la union de palabras
    handleStemming = StructureStemming()
    handleStemming.add('educ', 'educacion')
    handleStemming.add('educa', 'educacionando')
    handleStemming.merge('educ','educa')
    assert handleStemming.getStemWords() == {'educ': [{'educacion': 1, 'educacionando': 1}, 2]}


def test_five():
    # Prueba del ordenamiento alfabeticop de la raices
    handleStemming = StructureStemming()
    handleStemming.add('educ', 'educacion')
    handleStemming.add('educ', 'educacion')
    handleStemming.add('educ', 'educa')
    handleStemming.add('corr', 'correr')
    handleStemming.sortStruture()
    assert handleStemming.getStemWords() == {'corr': [{'correr': 1}, 1], 'educ': [{'educacion': 2, 'educa': 1}, 3]}


def test_six():
    # Prueba del ordenamiento por peso palabras
    handleStemming = StructureStemming()
    handleStemming.add('educ', 'educacion')
    handleStemming.add('educ', 'educacion')
    handleStemming.add('educ', 'educa')
    handleStemming.add('corr', 'correr')
    handleStemming.sortStruture()
    assert handleStemming.getStemWords() == {'educ': [{'educacion': 2, 'educa': 1}, 3], 'corr': [{'correr': 1}, 1] }

def test_Seven():
    # Prueba de la union de palabras parametro es una lista
    handleStemming = StructureStemming()
    handleStemming.add('educ', 'educacion')
    handleStemming.add('educa', 'educacionando')
    handleStemming.add('edus', 'educacio')
    handleStemming.mergeList(['educ','educa', 'edus'])
    assert handleStemming.getStemWords() == {'educ': [{'educacion': 1, 'educacionando': 1, 'educacio': 1}, 3]}