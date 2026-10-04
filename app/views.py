from django.shortcuts import render,redirect,get_object_or_404
from django.db.models import Sum
from .models import Transaction

def index(request):
    filter_type = request.GET.get("category", "All")

    transactions = Transaction.objects.all().order_by("-id")

    if filter_type == "Income":
        transactions = transactions.filter(category="Income")

    elif filter_type == "Expense":
        transactions = transactions.filter(category="Expense")

    total_income = Transaction.objects.filter(
        category="Income"
    ).aggregate(
        total=Sum("amount")
    )["total"] or 0

    total_expense = Transaction.objects.filter(
        category="Expense"
    ).aggregate(
        total=Sum("amount")
    )["total"] or 0

    available_balance = total_income - total_expense

    data = {
        "transactions": transactions,
        "total_income": total_income,
        "total_expense": total_expense,
        "available_balance": available_balance,
        "filter_type": filter_type,
    }

    return render(request, "index.html", data)

def formm(request):
    if request.method == "POST":
        amount = request.POST.get("amount")
        category = request.POST.get("category")
        date = request.POST.get("date")
        description = request.POST.get("description")

        Transaction.objects.create(
            amount=amount,
            category=category,
            date=date,
            description=description
        )

        return redirect("index")
    return render(request, "formm.html")

def edit(request, id):
    transaction = get_object_or_404(Transaction, id=id)

    if request.method == "POST":
        transaction.amount = request.POST.get("amount")
        transaction.category = request.POST.get("category")
        transaction.date = request.POST.get("date")
        transaction.description = request.POST.get("description")
        transaction.save()

        return redirect("index")

    data = {
        "transaction": transaction
    }

    return render(request, "edit.html", data)


def delete(request, id):
    transaction = get_object_or_404(Transaction, id=id)

    if request.method == "POST":
        transaction.delete()

    return redirect("index")