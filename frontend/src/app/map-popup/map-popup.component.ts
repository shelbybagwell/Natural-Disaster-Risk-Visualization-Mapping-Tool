import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-map-popup',
  standalone: false,
  templateUrl: './map-popup.component.html',
  styleUrl: './map-popup.component.scss'
})
export class MapPopupComponent {
  @Input() data: any;
  @Output() close = new EventEmitter<void>();
}
