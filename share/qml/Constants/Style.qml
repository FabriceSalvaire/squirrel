/***************************************************************************************************
 *
 * Copyright (C) 2017 Fabrice Salvaire
 * Contact: http://www.fabrice-salvaire.fr
 *
 * This file is part of the Babel software.
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 **************************************************************************************************/

// cf. http://wiki.qt.io/Qml_Styling

pragma Singleton
import QtQuick 2.6

QtObject {

    property QtObject font_size: QtObject {
	property int tiny:   8
	property int small: 10
	property int base:  12
	property int large: 18
	property int huge:  20
    }

    property QtObject spacing: QtObject {
	property int xs:     1
	property int small:  5
	property int base:  10
	property int large: 20
	property int huge:  30

	property int xs_horizontal:     1
	property int small_horizontal:  5
	property int base_horizontal:  10
	property int large_horizontal: 20

	property int xs_vertical:       1
	property int small_vertical:    5
	property int base_vertical:    10
	property int large_vertical:   20
    }

}
