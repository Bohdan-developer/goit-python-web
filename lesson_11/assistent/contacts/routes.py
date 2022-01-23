from flask import render_template, url_for, redirect, abort, request, flash
from assistent import db, mail
from flask_login import login_required, current_user
from assistent.contacts.forms import ContactForm
from assistent.models import Contact
from assistent.contacts import contact_bp
from flask_mail import Message


@contact_bp.route('/')
def about():
    return render_template('about.html')


@contact_bp.route('/index_contact', methods=['GET', 'POST'])
@login_required
def index_contact():
    form = ContactForm()
    if form.validate_on_submit():
        contact = Contact(name=form.name.data, phone=form.phone.data, email=form.email.data, birthday=form.birthday.data,
                          address=form.address.data, author=current_user)
        db.session.add(contact)
        db.session.commit()

        return redirect(url_for('contacts.index_contact'))
    contacts = Contact.query.filter_by(author=current_user).all()
    return render_template('index_contact.html', title="home page", form=form, contacts=contacts)


@contact_bp.route('/contact/<int:contact_id>', methods=['GET', 'POST'])
@login_required
def contact(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    return render_template('contact.html', contact=contact)


@contact_bp.route("/contact/<int:contact_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_contact(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    db.session.delete(contact)
    db.session.commit()
    return redirect(url_for('contacts.index_contact'))


@contact_bp.route("/contact/<int:contact_id>/update", methods=['GET', 'POST'])
@login_required
def update_contact(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    if contact.author != current_user:
        abort(403)
    form = ContactForm()
    if form.validate_on_submit():
        contact.name = form.name.data
        contact.phone = form.phone.data
        contact.email = form.email.data
        contact.birthday = form.birthday.data
        contact.address = form.address.data
        db.session.commit()
        flash('Your note has been updated!', 'success')
        return redirect(url_for('contacts.index_contact', contact_id=contact.id))
    elif request.method == 'GET':
        form.name.data = contact.name
        form.phone.data = contact.phone
        form.email.data = contact.email
        form.birthday.data = contact.birthday
        form.address.data = contact.address
    return render_template('index_contact.html', form=form)


@contact_bp.route("/contacts/<int:contact_id>/email", methods=['GET', 'POST'])
@login_required
def send_email(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    if contact.author != current_user:
        abort(403)
    msg = Message('Contact!',
                  recipients=[current_user.email],
                  body=str(contact))

    mail.send(msg)
    flash('Your note has been send!', 'success')
    return render_template('email.html')
