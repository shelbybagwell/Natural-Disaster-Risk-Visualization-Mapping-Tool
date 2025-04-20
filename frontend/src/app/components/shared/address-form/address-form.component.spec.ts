import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddressFormComponent } from './address-form.component';
import { MatButtonModule } from '@angular/material/button';
import { ReactiveFormsModule } from '@angular/forms';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';

describe('AddressFormComponent', () => {
  let component: AddressFormComponent;
  let fixture: ComponentFixture<AddressFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        MatFormFieldModule,
        MatInputModule,
        MatButtonModule,
        ReactiveFormsModule,
      ],
      declarations: [AddressFormComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AddressFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('look up button', () => {
    it('should call the api service and pass in address information', () => {
      //arrange

      //act

      //assert
    });

    it('should be disabled if address form not valid', () => {
      //arrange

      //act

      //assert
    });
  });

  describe('save button', () => {
    it('should call api service to save address if user logged in', () => {
      //arrange

      //act

      //assert
    });

    it('should be disabled if user not logged in', () => {
      //arrange

      //act

      //assert
    });
  });

  describe('cancel button', () => {
    it('should reset the form when cancel button is called', () => {
      //arrange
      component.addressForm.setValue({
        streetAddress: '777 Lucky St',
        city: 'Huntsville',
        state: 'AL',
        zip: '35757',
      });

      //act
      component.cancel();

      //assert
      expect(component.addressForm.value).toEqual({
        streetAddress: null,
        city: null,
        state: null,
        zip: null,
      });
    });

    it('should be disabled if form is clean', () => {
      //arrange

      //act

      //assert
    });
  });
});
