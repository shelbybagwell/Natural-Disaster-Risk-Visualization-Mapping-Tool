import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MenuComponent } from './menu.component';
import { MatIconTestingModule } from '@angular/material/icon/testing';
import { MatIconModule } from '@angular/material/icon';
import { ReactiveFormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatMenuModule } from '@angular/material/menu';

describe('MenuComponent', () => {
  let component: MenuComponent;
  let fixture: ComponentFixture<MenuComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        MatIconModule,
        MatMenuModule,
        MatFormFieldModule,
        MatInputModule,
        MatButtonModule,
        ReactiveFormsModule,],
      declarations: [MenuComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MenuComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  describe('open menu', () => {
    it('should call openMenu on the trigger when called', () => {
      //arrange
      spyOn(component.trigger, 'openMenu');
      //act
      component.openMenu();
      //assert
      expect(component.trigger.openMenu).toHaveBeenCalled();
    });
  });

  describe('view Map', () => {
    it('should take users to "/" or map component when called', () => {
      //arrange
      spyOn(component.router, 'navigateByUrl');
      //act
      component.viewMap();
      //assert
      expect(component.router.navigateByUrl).toHaveBeenCalledWith('/');
    });

    it('should be disabled when on the maps component', () => {
      //arrange

      //act

      //assert
    });
  });
});
