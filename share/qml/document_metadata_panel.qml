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

import QtQuick 2.7
import QtQuick.Controls 1.4
import QtQuick.Controls.Styles 1.4
import QtQuick.Layouts 1.3

Rectangle {
    id: document_metadata_panel
    anchors.fill: parent
    color: application_style.window_color

    /* ScrollView { */
    /*     horizontalScrollBarPolicy: Qt.ScrollBarAlwaysOff */

    Column {
        anchors.horizontalCenter: parent.horizontalCenter
        width: document_metadata_panel.width - 20
        // padding: 50
        spacing: 10

        TextArea {
            width: parent.width
            height: contentHeight * 1.1
            // placeholderText: qsTr('Enter title')
            text: qsTr("Title ...")
        }

        Row { // RowLayout
            width: parent.width
            spacing: 10
            Text {
                id: author_label
                // Layout.alignment: Qt.AlignTop
                text: qsTr('Author')
            }
            TextArea {
                // Layout.alignment: Qt.AlignTop
                // Layout.fillWidth: true
                width: parent.width - author_label.width - 10
                text: '...'
                height: contentHeight * 1.1
            }
        }
    }
    // }
}
