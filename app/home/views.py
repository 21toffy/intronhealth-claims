from flask import flash, jsonify, render_template, redirect, request, url_for

from app.models import Claim, Service, User
from . import home as home_blueprint
from app.forms import AddUser
from app import database
from datetime import datetime
import datetime as dt




@home_blueprint.route('/', methods=['GET'])
def home():

    return render_template('home/index.html')

@home_blueprint.route('/all/users', methods=['GET'])
def all_users():
    """
    List all Users
    """
    all_users = User.query.all()
    return render_template('home/home.html', users=all_users, title="Users")

@home_blueprint.route('/user/<int:id>', methods=['GET', 'POST'])
def view_user(id):
    """
        A route that allows claim officer fillout a form for a particular user
    """
    user_data = User.query.get(int(id))
    return render_template('home/user_data.html', user_data=user_data)

@home_blueprint.route('/user/<int:id>/edit', methods=['GET', 'POST'])
def edit_user(id):
    """
        A route for editing a user record
    """
    form = AddUser()

    user_data = User.query.get(int(id))

    if request.method == 'POST':
        name = request.form.get('name')
        gender = request.form.get('gender')
        salary = request.form.get('salary')
        date_of_birth = request.form.get('date_of_birth')

        dt_obj = datetime.strptime(date_of_birth, '%Y-%m-%d')

        if form.validate_on_submit():
            user_data.name = name
            user_data.gender = gender
            user_data.salary = salary
            user_data.date_of_birth = dt_obj

            database.session.commit()

            flash('User updated successfully.', 'success')
            return redirect(url_for('home.edit_user', id=user_data.id))

    return render_template('home/edit_user.html', user_data=user_data, form=form)

@home_blueprint.route('users/add', methods=['GET', 'POST'])
def add_user():
    """
        A route for adding users

    """
    form = AddUser()

    if request.method == 'POST':
        name = request.form.get('name')
        gender = request.form.get('gender')
        salary = request.form.get('salary')
        date_of_birth = request.form.get('date_of_birth')

        dt_obj = datetime.strptime(date_of_birth, '%Y-%m-%d')

        if form.validate_on_submit():
            try:
                new_user = User(name=name, gender=gender, salary=salary, date_of_birth=dt_obj)
                database.session.add(new_user)
                database.session.commit()

                flash('User created successfully.', 'success')
                return redirect(url_for('home.all_users'))
            except Exception as e:
                print(e, type(e))
                flash(f'{str(e)}', 'danger')
            

        flash('You entered and invalid form data', 'danger')
        return render_template('home/create_user.html', form=form)
    else:
        
        return render_template('home/create_user.html', form=form)

@home_blueprint.route('/user/<int:id>/delete', methods=['POST'])
def delete_user(id):
    """
        A route for deleting a user
    """
    user_data = User.query.get(int(id))
    database.session.delete(user_data)
    database.session.commit()

    flash('User deleted successfully.', 'success')
    return redirect(url_for('home.all_users'))


@home_blueprint.route('claim', methods=['GET'])
def claim():
    """
    List all Claims
    """
    all_claims = Claim.query.all()
    return render_template('home/claim.html', claims=all_claims, title="Claims")

@home_blueprint.route('create_claim', methods=['GET', 'POST'])
def create_claim():
    """
        A route for a claim officer to make/create a claim
    """

    if request.method == 'POST':
        # Get the form field values for claim model insertion

        user = request.form.get('user')
        diagnosis = request.form.get('diagnosis')
        hmo = request.form.get('hmo')

        total_cost = request.form.get('total_cost')
        service_charge = request.form.get('service_charge')
        final_cost = request.form.get('final_cost')


        user = User.query.filter_by(name=user).first()
        new_claim = Claim(user_id=user.id, diagnosis=diagnosis, hmo=hmo, service_charge=service_charge,total_cost=total_cost, final_cost=final_cost)
        database.session.add(new_claim)
        database.session.commit()

        # Get the form field values for service model insertion
        service_name = request.form.getlist('service_name')
        service_type = request.form.getlist('type')
        # service_types = request.form.getlist('type{}'.format(i))

        provider_name = request.form.getlist('provider_name')
        source = request.form.getlist('source')
        cost_of_service = request.form.getlist('cost_of_service')

        dates = request.form.getlist('service_date')
        print(dates)

        # Formate dates
        service_date = []
        for d in dates:
            service_date.append(datetime.strptime(d, '%Y-%m-%d'))

        # Get the above claim as foreign key for services
        claim = Claim.query.order_by(Claim.id.desc()).first()


        # Loop to enter possible list of services
        for i in range(len(service_name)):
            new_service = Service(claim_id=claim.id,
                                  service_date=service_date[i],
                                  service_name=service_name[i],
                                  service_type=service_type[0],
                                  provider_name=provider_name[i],
                                  source_hospital=source[i],
                                  cost_of_service=cost_of_service[i])
            database.session.add(new_service)
            database.session.commit()

        flash('Claim created successfully.', 'success')
        return redirect(url_for('home.claim'))
    else:
        all_users = User.query.with_entities(User.name).all()
        print(all_users)
        return render_template('home/create_claim.html', all_users=all_users)

@home_blueprint.route('/claim/<int:id>', methods=['GET', 'POST'])
def view_claim(id):
    """
        A route that allows claim to be viewed
    """
    claim_data = Claim.query.get(int(id))
    return render_template('home/claim_data.html', claim_data=claim_data)


@home_blueprint.route('create_claim/age/', methods=['POST'])
def user_age():
    """
        A route to get a user's birthdate
        and calculate his age 
    """
    if request.method == "POST":
        data = request.form.get("age").strip()
        user = User.query.filter_by(name=data).first()
        age = (dt.date.today().year - user.date_of_birth.year)
        print(age)
 
    
    return jsonify({'age': age})





@home_blueprint.route('/claim/<int:id>/delete', methods=['POST'])
def delete_claim(id):
    claim = Claim.query.get(id)

    if not claim:
        flash('Claim not found.', 'error')
        return redirect(url_for('home.claim'))  # Redirect to the page listing all claims

    try:
        # Delete the claim and its associated services
        for service in claim.services:
            database.session.delete(service)
        database.session.delete(claim)
        database.session.commit()
        flash('Claim and its services have been deleted.', 'success')
    except Exception as e:
        print(str(e))
        database.session.rollback()
        flash('An error occurred while deleting the claim.', 'error')

    return redirect(url_for('home.claim'))  # Redirect to the page listing all claims



@home_blueprint.route('/claim/<int:id>/edit', methods=['GET', 'POST'])
def edit_claim(id):
    """
    Route for editing a claim record.

    Args:
        id (int): The ID of the claim to be edited.

    Returns:
        If a GET request:
            Renders the claim editing page with pre-filled form fields and calculated costs.
        If a POST request:
            Processes the form submission, updates the claim and associated services, and redirects to the claims page.
    """
    form = AddUser()

    # Retrieve claim data and user data
    claim_data = Claim.query.get(int(id))
    all_users = User.query.with_entities(User.name).all()

    default_service_types = ["Hematology", "Microbiology", "Chemical Pathology", "Histopathology", "Immunology"]

    if request.method == 'POST':
        # Handle form submission and update claim data
        service_ids = [row.id for row in claim_data.services]
        user = request.form.get('user')
        diagnosis = request.form.get('diagnosis')
        hmo = request.form.get('hmo')

        total_cost = request.form.get('total_cost')
        service_charge = request.form.get('service_charge')
        final_cost = request.form.get('final_cost')

        if claim_data:
            service_ids = [service.id for service in claim_data.services]            
            service_value_map = {service_id: request.form.get(f'{service_id}type') for service_id in service_ids}


        user = User.query.filter_by(name=user).first()
        claim_data.user_id=user.id
        claim_data.diagnosis=diagnosis
        claim_data.hmo=hmo
        claim_data.service_charge=service_charge
        claim_data.total_cost=total_cost
        claim_data.final_cost=final_cost
        database.session.commit()

        # Retrieve form field values for service model insertion
        service_name = request.form.getlist('service_name')
        provider_name = request.form.getlist('provider_name')
        source = request.form.getlist('source')
        cost_of_service = request.form.getlist('cost_of_service')

        dates = request.form.getlist('service_date')
        print(
            service_name,
            service_ids,
            service_value_map
        )

        # Formate dates
        service_date = []
        for d in dates:
            service_date.append(datetime.strptime(d, '%Y-%m-%d'))

        # Get the above claim as foreign key for services
        claim = Claim.query.order_by(Claim.id.desc()).first()
        # Loop to enter possible list of services
        for ind, serv_id in enumerate(service_ids):
            service = Service.query.get(int(serv_id))
            if service:
                service.service_name = service_name[ind]
                service.service_type = service_value_map[serv_id]
                service.provider_name = provider_name[ind]
                service.source_hospital = source[ind]
                service.cost_of_service = cost_of_service[ind]
                service.service_date = service_date[ind] 
                database.session.commit()
        return redirect(url_for('home.claim'))
    
    # Calculate total cost, service charge, and final cost    
    total_cost = sum(int(service.cost_of_service) for service in claim_data.services)
    service_charge = int(total_cost * 0.1)
    final_cost = int(total_cost + service_charge)

    return render_template('home/edit_claim.html', all_users=all_users, claim_data=claim_data, form=form,
                           default_service_types=default_service_types,
                           total_cost=total_cost, service_charge=service_charge, final_cost=final_cost)






