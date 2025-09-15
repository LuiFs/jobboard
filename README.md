<h1> Instruções </h1>

1. Clone o projeto no github;
2. Caso necessário crie um venv ```python3 -m venv venv``` e o ative ```.\venv\Scripts\activate```;
3. Caso crie uma venv, utilize ```pip install Django e pip install behave-django```;
4. Crie um super usuário, utilize ```python manage.py createsuperuser```;
   * Utilize email como login;
   * Para criar digite email e senha;
5. Para inicializar a aplicação utilize ```python manage.py runserver```;
6. Após realizar o login na aplicação, para criar um novo usuário **Empresa** e/ou **Candidato** coloque ao final da url ```/admin```;
   * Para criar empresa marque a opção ```is_company```;
8. Para realizar o teste utilize ```python manage.py test```.

<h2>Observações</h2>

Os códigos de views, urls, models etc, estão dentro da pasta **core**; <br>
Frontend apenas para a utilização das funcionalidades, ou seja, não está bonito.
