# Proyecto Gestor Académico – 2C-2025

Universidad Argentina de la Empresa (UADE)  
Departamento de Tecnología – Informática  
Programación I / Algoritmos y Estructura de Datos I  
Profesor: Ing. María Eugenia Varando  
Día de cursada: Miercoles  
Turno: Tarde

---

## Integrantes
* Cinti Valentino – Legajo 1213639
* Feigelman Iair – Legajo 1223083
* Holm Ian – Legajo 1214983
* Méndez Milena Luciana – Legajo 1214694
* Sampieri Juan Francisco – Legajo 1214467

---

## Objetivo del Proyecto
Desarrollar un gestor académico que, además de incluir la gestión básica de materias, incorpore metas y herramientas gamificadas para incentivar el estudio de manera interactiva y motivadora.

---

## Alcance – 1era Etapa
En esta primera etapa, el proyecto se centrará en implementar la lógica principal del manejo de materias, lo cual incluye:
* Gestión de materias.
* Registro y seguimiento de notas.
* Administración de correlatividades.
* Uso de una matriz homogénea compuesta por las materias correlativas, donde se utiliza 1 para cuando es correlativa y 0 para cuando no lo es.

---

## Resumen Funcional del Sistema

Este proyecto es un **sistema de gestión académica** basado en menús de consola. Está diseñado para gestionar la vida académica de estudiantes y las tareas administrativas de un administrador.

El sistema maneja entidades como **Usuarios**, **Materias**, **Calendario** (horarios), **Notas** y **Flashcards** (tarjetas de estudio). También incluye un sistema de **Logs** para registrar acciones importantes y **errorLogs** para los errores.

### Roles de Usuario

El sistema define dos tipos de roles con permisos y menús completamente diferentes:

1.  **Estudiante (Rol: "User")**
    * Es el rol principal del sistema, enfocado en la **gestión de la propia carrera**.
    * **Permisos:** Anotarse y darse de baja de materias, cargar sus notas, consultar su calendario, ver su promedio, y utilizar el módulo de Flashcards para estudiar o proponer nuevas tarjetas.

2.  **Administrador (Rol: "Administrator")**
    * Es el rol de **supervisión y mantenimiento** del sistema.
    * **Permisos:** Dar de baja a usuarios, cambiar el rol de un usuario (ascender a admin o degradar a estudiante), aprobar las Flashcards propuestas por los estudiantes, y generar reportes generales del sistema.

### Menús

#### 1. Menú de Acceso (`menuLoginPrincipal`)

Es la primera pantalla que ve el usuario. Ofrece tres opciones:
* **1- Iniciar sesión:** Permite a un usuario existente ingresar (`inicioDeSesion`), con un límite de 3 intentos.
* **2- Crear usuario:** Inicia el flujo para registrar un nuevo usuario (`altaUsuario`).
* **3- Salir:** Cierra la aplicación.

#### 2. Menú Principal (Dinámico) (`menuInicial` y `menuPrincipal`)

Una vez que el usuario inicia sesión, el sistema detecta su rol y le presenta un menú principal dinámico.

**Menú de Estudiante:**
* `1- Anotarse a materias`
* `2- Estado 'Pack de 5 materias'` (Inscripción automática a 5 materias)
* `3- Cargar nota de materia`
* `4- Dar de baja una materia`
* `5- Ver calendario`
* `6- Ver notas`
* `7- Ver promedio de carrera`
* `8- Practicar con Flashcards` (Abre un sub-menú)
* `9- Ajustes` (Cambiar contraseña o cerrar sesión)
* `0- Salir`

**Menú de Administrador:**
* `1. Baja de usuario`
* `2. Cambiar rol de usuario`
* `3. Procesar flashcards` (Revisar y aprobar flashcards pendientes)
* `4. Generar reporte` (Abre un sub-menú de reportes)
* `5. Ajustes` (Cambiar contraseña o cerrar sesión)
* `0. Salir`

---

## Repositorio
[GitHub – Proyecto Gestor Académico](https://github.com/IairFei/Proyecto-P1)

---

## Bibliografía
*(se completará durante el desarrollo del proyecto)*

---

## Tecnologías & Herramientas
* Lenguaje de programación: **Python**
* Control de versiones: **Git + GitHub**


---

## Cronograma Tentativo
1.  Etapa 1 – Lógica de materias y correlatividades.
2.  Etapa 2 – Sistema de metas y gamificación.