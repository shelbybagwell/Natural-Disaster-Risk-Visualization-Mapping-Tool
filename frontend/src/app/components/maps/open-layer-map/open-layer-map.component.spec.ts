import { ComponentFixture, TestBed } from '@angular/core/testing';
import * as olProj from 'ol/proj';
import { OpenLayerMapComponent } from './open-layer-map.component';
import { getCenter } from 'ol/extent';

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

  describe('create map in afterViewInit', () => {
    it('should create a map on load', () => {
      expect(component.map).toBeTruthy();
    });

    it('should create a map with passed in coordinates', () => {
      //arrange
      component.centerPoint = [123.4321, 21.1234];
      //act
      component.ngAfterViewInit();
      let mapCenter = component.map.getView().getCenter()!;
      let centerLonLat = olProj.toLonLat(mapCenter);
      //assert
      expect(centerLonLat.toString()).toContain(component.centerPoint.toString());
    });
  });
});
