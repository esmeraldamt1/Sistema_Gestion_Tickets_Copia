# 📦 Importamos JsonResponse para enviar respuestas en formato JSON
from django.http import JsonResponse

# 📦 Decorador para desactivar la protección CSRF (para permitir solicitudes desde clientes sin sesión)
from django.views.decorators.csrf import csrf_exempt

# 📦 Decorador para aplicar csrf_exempt a métodos dentro de clases
from django.utils.decorators import method_decorator

# 📦 Clase base para vistas basadas en clases (CBV)
from django.views import View

# 📦 Módulo para trabajar con datos en formato JSON
import json

# 📦 Importamos el modelo Departamento desde models.py
from .models import Departamento


# 📘 Vista basada en clase para listar y crear departamentos
@method_decorator(csrf_exempt, name='dispatch')  # Desactiva CSRF para todos los métodos de esta clase
class ListaDepartamentos(View):
    """
    Vista que permite:
    - GET: listar todos los departamentos
    - POST: crear un nuevo departamento
    """

    def get(self, request):
        """
        Método GET para listar todos los departamentos.
        Retorna lista con ID y nombre.
        """
        departamentos = Departamento.objects.all().only("id", "nombre")  # Consulta todos los departamentos, solo campos necesarios
        data = [{"id": str(dep.id), "nombre": dep.nombre} for dep in departamentos]  # Serializa cada uno a diccionario
        return JsonResponse(data, safe=False, status=200)  # safe=False permite devolver una lista

    def post(self, request):
        """
        Método POST para crear un nuevo departamento.
        Espera JSON con campo 'nombre'.
        """
        try:
            data = json.loads(request.body)  # Intenta convertir el cuerpo de la solicitud a dict
            nombre = data.get("nombre")  # Extrae el campo 'nombre'

            if not nombre:
                return JsonResponse({"error": "El campo 'nombre' es obligatorio"}, status=400)

            if Departamento.objects(nombre=nombre).first():
                return JsonResponse({"error": "El departamento ya existe"}, status=400)

            nuevo_departamento = Departamento(nombre=nombre)  # Crea instancia
            nuevo_departamento.save()  # Guarda en la base de datos

            return JsonResponse({
                "message": "Departamento creado con éxito",
                "id": str(nuevo_departamento.id)
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Formato JSON inválido"}, status=400)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


# 📘 Vista basada en función para crear un solo departamento
@csrf_exempt  # Desactiva CSRF para esta función
def departamento_create(request):
    """
    Vista que permite crear un solo departamento.
    Espera JSON con el campo 'nombre'.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nombre = data.get("nombre")

            if not nombre:
                return JsonResponse({"error": "El campo 'nombre' es obligatorio"}, status=400)

            if Departamento.objects(nombre=nombre).first():
                return JsonResponse({"error": "El departamento ya existe"}, status=400)

            nuevo_departamento = Departamento(nombre=nombre)
            nuevo_departamento.save()

            return JsonResponse({
                "message": "Departamento creado con éxito",
                "id": str(nuevo_departamento.id)
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Formato JSON inválido"}, status=400)
    else:
        return JsonResponse({"error": "Método no permitido"}, status=405)


# 📘 Vista basada en función para crear múltiples departamentos
@csrf_exempt  # Desactiva CSRF para esta función
def departamentos_create_bulk(request):
    """
    Crea múltiples departamentos a partir de una lista de objetos JSON.
    Espera: [{ "nombre": "TI" }, { "nombre": "Soporte" }]
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            if not isinstance(data, list):
                return JsonResponse({"error": "Se espera una lista de departamentos"}, status=400)

            departamentos_creados = []  # Lista de departamentos creados
            errores = []  # Lista de errores individuales

            for idx, dep_data in enumerate(data):  # Iteramos por cada objeto
                nombre = dep_data.get("nombre")

                if not nombre:
                    errores.append({"index": idx, "error": "El campo 'nombre' es obligatorio"})
                    continue

                if Departamento.objects(nombre=nombre).first():
                    errores.append({"index": idx, "error": f"El departamento '{nombre}' ya existe"})
                    continue

                nuevo_dep = Departamento(nombre=nombre)
                nuevo_dep.save()
                departamentos_creados.append({
                    "id": str(nuevo_dep.id),
                    "nombre": nuevo_dep.nombre
                })

            return JsonResponse({
                "departamentos_creados": departamentos_creados,
                "errores": errores
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Formato JSON inválido"}, status=400)

    else:
        return JsonResponse({"error": "Método no permitido"}, status=405)
