import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MapContainerComponent } from './map-container.component';
import { MatIconModule } from '@angular/material/icon';
import { MatMenuModule } from '@angular/material/menu';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { ReactiveFormsModule } from '@angular/forms';
import { OpenLayerMapComponent } from '../open-layer-map/open-layer-map.component';
import { AddressFormComponent } from '../../shared/address-form/address-form.component';

describe('MapContainerComponent', () => {
  let component: MapContainerComponent;
  let fixture: ComponentFixture<MapContainerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        MatIconModule,
        MatMenuModule,
        MatFormFieldModule,
        MatInputModule,
        MatButtonModule,
        ReactiveFormsModule,
      ],
      declarations: [
        MapContainerComponent,
        OpenLayerMapComponent,
        AddressFormComponent
      ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MapContainerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
