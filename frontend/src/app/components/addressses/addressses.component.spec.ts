import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddresssesComponent } from './addressses.component';

describe('AddresssesComponent', () => {
  let component: AddresssesComponent;
  let fixture: ComponentFixture<AddresssesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [AddresssesComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AddresssesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
