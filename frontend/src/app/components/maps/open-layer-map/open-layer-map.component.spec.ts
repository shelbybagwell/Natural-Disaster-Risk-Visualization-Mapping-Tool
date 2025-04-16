import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OpenLayerMapComponent } from './open-layer-map.component';

describe('OpenLayerMapComponent', () => {
  let component: OpenLayerMapComponent;
  let fixture: ComponentFixture<OpenLayerMapComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [OpenLayerMapComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(OpenLayerMapComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
