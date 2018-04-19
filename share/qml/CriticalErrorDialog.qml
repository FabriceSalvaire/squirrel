/***************************************************************************************************
 *
 * Copyright (C) 2018 Fabrice Salvaire
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

import QtQuick 2.7
import QtQuick.Controls 1.4
import QtQuick.Controls.Styles 1.4
import QtQuick.Layouts 1.3
import QtQuick.Window 2.2

import Constants 1.0
// import Local 1.0

Item {
    id: critical_error

    width: 800
    height: 500

    signal accepted()
    signal rejected()
    signal exit_application()

    property string backtrace: ''

    Component.onCompleted: {
	accept_button.clicked.connect(accepted)
        exit_button.clicked.connect(exit_application)
    }

    RowLayout {
	anchors.fill: parent
        anchors.margins: Style.spacing.base
        spacing: Style.spacing.base

	// Text {
	//     id: title
	// }

	TextArea {
	    Layout.fillWidth: true
	    Layout.fillHeight: true
            readOnly: true
            textFormat: TextEdit.RichText
            text: backtrace
	}

	ColumnLayout {
            spacing: Style.spacing.base

            Item {
                Layout.fillHeight: true
            }

	    Button {
                id: exit_button
		text: qsTr('Exit Application')
	    }

	    Button {
		id: accept_button
               	text: qsTr('Ok')
	    }
	}
    }
}
