from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Paper, CustomUser
from .forms import RegisterForm, LoginForm, PaperForm

# ---------------------------
# HOME PAGE (ROLE SELECTION)
# ---------------------------
def index(request):
    return render(request, 'papers/index.html')


# ---------------------------
# LOGIN
# ---------------------------
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Redirect based on role
            if user.role == "student":
                return redirect("student_dashboard")
            elif user.role == "teacher":
                return redirect("teacher_dashboard")
            elif user.role == "admin":
                return redirect("admin_dashboard")

            return redirect("index")
    else:
        form = LoginForm()
    return render(request, "papers/login.html", {"form": form})


# ---------------------------
# LOGOUT
# ---------------------------
def logout_view(request):
    logout(request)
    return redirect("index")


# ---------------------------
# REGISTER
# ---------------------------
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            messages.success(request, "Account created successfully.")
            return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "papers/register.html", {"form": form})


# ---------------------------
# STUDENT DASHBOARD
# ---------------------------
@login_required
def student_dashboard(request):
    papers = Paper.objects.filter(student=request.user)
    return render(request, "papers/student_dashboard.html", {"papers": papers})


# ---------------------------
# TEACHER DASHBOARD
# ---------------------------
@login_required
def teacher_dashboard(request):
    papers = Paper.objects.filter(teacher=request.user)
    return render(request, "papers/teacher_dashboard.html", {"papers": papers})


# ---------------------------
# ADMIN DASHBOARD
# ---------------------------
@login_required
def admin_dashboard(request):
    if request.user.role != "admin":
        return redirect("index")

    users = CustomUser.objects.all()
    papers = Paper.objects.all()

    return render(request, "papers/admin_dashboard.html", {
        "users": users,
        "papers": papers
    })


# ---------------------------
# UPLOAD PAPER
# ---------------------------
@login_required
def upload(request):
    if request.user.role != "student":
        return redirect("index")

    if request.method == "POST":
        form = PaperForm(request.POST, request.FILES)

        if form.is_valid():
            file = request.FILES['file']

            paper = form.save(commit=False)
            paper.student = request.user

            paper.file_name = file.name
            paper.file_data = file.read()  

            paper.save()

            return redirect("student_dashboard")
    else:
        form = PaperForm()

    return render(request, "papers/upload.html", {"form": form})


# ---------------------------
# PAPER DETAIL PAGE
# ---------------------------
@login_required
def detail(request, pk):
    paper = get_object_or_404(Paper, pk=pk)
    return render(request, "papers/detail.html", {"paper": paper})



# ---------------------------
# REVIEW PAPER (Teacher Only)
# ---------------------------
@login_required
def review_paper(request, pk):
    paper = get_object_or_404(Paper, pk=pk)

    if request.user.role != "teacher":
        return redirect("index")

    if request.method == "POST":
        paper.feedback = request.POST.get("feedback")
        paper.grade = request.POST.get("grade")
        paper.status = request.POST.get("status")
        paper.save()

        return redirect("teacher_dashboard")

    return render(request, "papers/review.html", {"paper": paper})
